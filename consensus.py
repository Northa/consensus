# https://github.com/Northa/consensus/
from urllib import request
from sys import exit
from json import loads
import math
from collections import defaultdict
import os


ERR_MSG = f"\033[91m[ERR] API endpoint unreachable: _err_api_\n" \
          f"[ERR] Be sure you have enabled your API " \
          f"(you can enable this in your app.toml config file)\n" \
          f"Bugreports github: https://github.com/Northa/consensus/\033[0m"

# default ports
RPC = "http://127.0.0.1:26657"
REST = "http://127.0.0.1:1317"

def handle_request(api: str, pattern: str):
    try:
        response = loads(request.urlopen(f"{api}/{pattern}").read())
        return response if response is not None else exit(ERR_MSG.replace('api', api))

    except Exception as err:
        ERR_MSG.replace('_err_api_', api)
        err = f"url: {api}/{pattern} err: {err}"
        exit(f"{ERR_MSG}\n{err}")


# def clear_cls():
#     os.system('cls' if os.name=='nt' else 'clear')


def get_validator_votes():
    validator_votes = []
    votes = STATE['result']['round_state']['votes']
    height = STATE['result']['round_state']['height']
    step = STATE['result']['round_state']['step']
    cur_round = STATE['result']['round_state']['round']
    chain = get_chain_id()
    proposer = STATE['result']['round_state']['validators']['proposer']['pub_key']['value']
    for r_ound in votes:
        if int(r_ound['round']) != cur_round:
            continue

        if float(r_ound['prevotes_bit_array'].split('=')[-1].strip()) > 0:
            print(F"\nChain-id: {chain}\nHeight: {height} Round: {r_ound['round']} step: {step}\nprevotes_bit_array: {r_ound['prevotes_bit_array'].split('} ')[-1]}")
            for prevote in r_ound['prevotes']:
                try:
                    app_hash = prevote.split("Prevote) ")[1].split(" ")[0][:3]
                    # app_hash = f"{hashlib.sha256(app_hash.encode('utf-8')).hexdigest()[:3]}"
                    val_vote = prevote.split('@')[0].split(':')[1].split(' ')[0]
                    validator_votes.append([val_vote, app_hash])
                except IndexError:
                    validator_votes.append(prevote)
    if len(validator_votes) > 0:
        return validator_votes, proposer
    exit(f"height: {height} round: {cur_round} No votes found. Try in a few seconds")


def get_validators():
    validators = []
    state_validators = STATE['result']['round_state']['validators']['validators']
    for val in state_validators:
        res = val['address'], val['voting_power'], val['pub_key']['value']
        validators.append(res)
    return validators


def get_bonded():
    result = handle_request(REST, '/cosmos/staking/v1beta1/pool')['pool']
    return result


def strip_emoji_non_ascii(moniker):
    moniker = "".join([letter for letter in moniker if letter.isascii()])
    return moniker[:15].strip().lstrip()


def get_validators_rest(proposer=None):
    validator_dict = dict()
    bonded_tokens = int(get_bonded()["bonded_tokens"])
    validators = handle_request(REST, '/cosmos/staking/v1beta1/validators?status=BOND_STATUS_BONDED&pagination.limit=2000')

    for validator in validators['validators']:

        validator_vp = int(validator["tokens"])
        vp_percentage = round((100 / bonded_tokens) * validator_vp, 3)
        moniker = validator["description"]["moniker"][:15].strip()
        moniker = strip_emoji_non_ascii(moniker)
        validator_dict[validator["consensus_pubkey"]["key"]] = {
                                 "moniker": moniker,
                                 "address": validator["operator_address"],
                                 "status": validator["status"],
                                 "voting_power": validator_vp,
                                 "voting_power_perc": f"{vp_percentage}%",
                                 "voting_power_perc1": vp_percentage}
        if proposer in validator["consensus_pubkey"]["key"]:
            proposer = moniker

    return validator_dict, proposer


def merge():
    votes, proposer = get_validator_votes()
    validators = get_validators()
    votes_and_vals = list(zip(votes, validators))
    # print(votes_and_vals)
    validator_rest, proposer = get_validators_rest(proposer)

    final_list = []

    for k, v in votes_and_vals:
        if v[2] in validator_rest:
            validator_rest[v[2]]['voted'] = k
            final_list.append(validator_rest[v[2]])

    return final_list, proposer


def list_columns(obj, cols=3, columnwise=True, gap=8):
    # thnx to https://stackoverflow.com/a/36085705

    sobj = [str(item) for item in obj]
    if cols > len(sobj): cols = len(sobj)
    max_len = max([len(item) for item in sobj])
    if columnwise: cols = int(math.ceil(float(len(sobj)) / float(cols)))
    plist = [sobj[i: i+cols] for i in range(0, len(sobj), cols)]
    if columnwise:
        if not len(plist[-1]) == cols:
            plist[-1].extend(['']*(len(sobj) - len(plist[-1])))
        plist = zip(*plist)
    printer = '\n'.join([
        ''.join([c.ljust(max_len + gap) for c in p])
        for p in plist])
    return printer


def get_chain_id():
    response = handle_request(REST, '/cosmos/base/tendermint/v1beta1/node_info')
    # for i in response:print()
    chain_id = response['default_node_info']['network'] if 'default_node_info' in response else response['node_info']['network']
    return chain_id


def colorize_output(validators):
    result = []
    validators = sorted(validators, key=lambda x: x['voting_power'], reverse=True)
    for num, val in enumerate(validators):
        vp_perc = f"{val['voting_power_perc']:<12}"
        moniker = val['moniker']

        if val['voted'] != 'nil-Vote':
            stat = f"\033[92m{num+1:<3} {'ONLINE':<8} \033[0m"
            # stat = f"{num+1:<3} {'🟢':<2}"
            app_hash = f"{val['voted'][1]}".upper()

            result.append(f"{stat} {moniker:<16}{app_hash} {vp_perc}")

        else:
            stat = f"\033[91m{num+1:<3} {'OFFLINE':<8} \033[0m"
            # stat = f"{num+1:<3} {'🔴':<2}"
            result.append(f"{stat} {moniker:<16}--- {vp_perc}")

    return result


def calculate_colums(result):
    if len(result) <= 30:
        return list_columns(result, cols=1)
    elif 30 < len(result) <= 60:
        return list_columns(result, cols=2)
    elif 60 < len(result) <= 150:
        return list_columns(result, cols=3)
    else:
        return list_columns(result, cols=4)


# def get_pubkey_by_valcons(valcons, height):
#     response = handle_request(REST, f"/validatorsets/{height}")
#     for validator in response['result']['validators']:
#         if valcons in validator['address']:
#             return validator['pub_key']['value']


# def get_moniker_by_pub_key(pub_key, height):
#     response = handle_request(REST, f"cosmos/staking/v1beta1/historical_info/{height}")
#     for validator in response['hist']['valset']:

#         if pub_key in validator['consensus_pubkey']['key']:
#             return strip_emoji_non_ascii(validator['description']['moniker'])


# def get_evidence(height):
#     evidences = handle_request(REST, '/cosmos/evidence/v1beta1/evidence')
#     for evidence in evidences['evidence']:
#         if int(height) - int(evidence['height']) < 1000:
#             pub_key = get_pubkey_by_valcons(evidence['consensus_address'], evidence['height']).strip()
#             moniker = get_moniker_by_pub_key(pub_key, evidence['height'])
#             # print(colored(f"Evidence: {moniker}\nHeight: {evidence['height']} {evidence['consensus_address']} power: {evidence['power']}\n", 'yellow'))
#             print(f"\033[93mEvidence: {moniker}\nHeight: {evidence['height']} {evidence['consensus_address']} power: {evidence['power']}\033[0m\n")


def main(STATE):
    validators, proposer = merge()
    online_vals = 0
    votes = defaultdict(float)
    for num, val in enumerate(validators):
        if val['voted'] == 'nil-Vote':
            votes['nil-Vote'] += val['voting_power_perc1']
        else:
            online_vals += 1
            votes[val['voted'][1]] += val['voting_power_perc1']
    print(f"Proposer: {proposer}")
    print('\nConsensus:')
    sum_vp = 0
    for k, v in votes.items():
        if not 'nil' in k:
            sum_vp += round(v,2)
            print(f"{f'hash {k}'}: {round(v,2):.2f}%")
        else:
            print(f"{k}: {round(v,2):.2f}%")

    print(f"\n{'Online_vp':<17}: {sum_vp:.2f}%")
    print(f"Online validators: {online_vals}/{len(validators)}\n")
    # get_evidence(STATE['result']['round_state']['height/round/step'])
    result = colorize_output(validators)
    print(calculate_colums(result))


if __name__ == '__main__':
    try:
        STATE = handle_request(RPC, 'dump_consensus_state')
        exit(main(STATE))
    except KeyboardInterrupt:
        exit(1)