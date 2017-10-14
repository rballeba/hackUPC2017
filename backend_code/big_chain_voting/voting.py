from bigchaindb_driver import BigchainDB
from bigchaindb_driver.crypto import generate_keypair

def _vote_token(question, voter_public_key):
    return {
        'data': {
            'token_for': {
                'vote': {
                    'identifier': ''.join(question.values()).strip(),
                    'org': org.public_key,
                    'voter': voter_public_key
                }
            }
        }
    }

def give_tokens(bdb, fr, to_public_key, question):
    prepared_token_tx = bdb.transactions.prepare(
        operation='CREATE',
        signers=org.public_key,
        recipients=[([u1.public_key],3)],
        asset=_vote_token(question, to_public_key),
    )
    fulfilled_token_tx = bdb.transactions.fulfill(
        prepared_token_tx,
        private_keys=org.private_key
    )

    send_token_tx = bdb.transactions.send(fulfilled_token_tx)
    return send_token_tx

def vote(bdb, voter, org_public_key, question_id, val):
    # primero encontramos el asset
    assets = bdb.assets.get(search=question_id)
    asset = next(x for x in assets
            if x['data']['token_for']['vote']['voter']==voter.public_key)

    asset_id = asset['id']

    # a partir del asset se consigue la contraseña
    txs = bdb.transactions.get(asset_id=asset_id)
    tx = next(x for x in txs
              if x['asset']['data']['token_for']['vote']['org']==org_public_key)

    output_index = 0
    output = tx['outputs'][output_index]

    transfer_input = {
        'fulfillment': output['condition']['details'],
        'fulfills' : {
            'output_index': output_index,
            'transaction_id': tx['id'],
        },
        'owners_before': output['public_keys'],
    }

    transfer_asset = {
        'id': tx['id']
    }

    prepared_transfer_tx = bdb.transactions.prepare(
        operation='TRANSFER',
        asset=transfer_asset,
        inputs=transfer_input,
        recipients=[([org.public_key], 1+val), ([u1.public_key],2-val)]
    )

    fulfilled_transfer_fx = bdb.transactions.fulfill(
        prepared_transfer_tx,
        private_keys=u1.private_key
    )

    sent_transfer_tx = bdb.transactions.send(fulfilled_transfer_fx)
    return sent_transfer_tx

def count_votes(bdb, org, question_id, census):
    c = set(census)
    assets = bdb.assets.get(search=question_id)
    # filtrdao de assets
    assets = [x for x in assets
                if x['data']['token_for']['vote']['org']==org.public_key]

    txs = []
    for asset in assets:
        lst = bdb.transactions.get(asset_id=asset['id'])

        # filtramos los resultados incorrectos
        lst = [x for x in lst
                if len(x['outputs']) > 1 and x['outputs'][1]['public_keys'][0] in census]

        txs += lst
    #return txs
    n_votes = len(txs)
    for_ = len([x for x in txs if x['outputs'][0]['amount'] == '2'])
    against = len([x for x in txs if x['outputs'][0]['amount'] == '1'])
    return {
        'votes': n_votes,
        'votes_for': for_,
        'votes_against': against,
    }
