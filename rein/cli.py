import json
import random
import string
import requests
import hashlib
import click
from datetime import datetime
from subprocess import check_output

from sqlalchemy import and_

from lib.ui import create_account, import_account, enroll, identity_prompt
from lib.user import User
from lib.bucket import Bucket, get_bucket_count, create_buckets
from lib.document import Document
from lib.placement import Placement, create_placements
from lib.validate import verify_sig
from lib.bitcoinecdsa import sign, pubkey
from lib.market import mediator_prompt, job_prompt, create_signed_document
import lib.config as config

rein = config.Config()


@click.group()
@click.option('--debug/--no-debug', default=False)
@click.pass_context
def cli(ctx, debug):
    if debug:
        click.echo("Debuggin'")
    pass


@cli.command()
@click.option('--multi/--no-multi', default=False, help="add even if an identity exists")
def setup(multi):
    """
    Setup or import an identity
    """
    log = rein.get_log()
    if multi:
        rein.set_multiuser()
    log.info('entering setup')
    if rein.has_no_account():
        click.echo("\nWelcome to Rein.\n"
                   "Do you want to import a backup or create a new account?\n\n"
                   "1 - Create new account\n2 - Import backup\n")
        choice = click.prompt("Choice", type=int, default=1)
        if choice == 1:
            create_account(rein)
            log.info('account created')
        elif choice == 2:
            import_account(rein)
            log.info('account imported')
        else:
            click.echo('Invalid choice')
            return
        click.echo("------------")
        click.echo("The file %s has just been saved with your user details and needs to be signed "
                   "with your master Bitcoin private key. The private key for this address should be "
                   "kept offline and multiple encrypted backups made. This key will effectively "
                   "become your identity in Rein and a delegate address will be used for day-to-day "
                   "transactions.\n\n" % rein.enroll_filename)
        res = enroll(rein)
        if res['valid']:
            click.echo("Enrollment complete. Run 'rein request' to request free microhosting to sync to.")
            log.info('enrollment complete')
        else:
            click.echo("Signature verification failed. Please try again.")
            log.error('enrollment failed')
    elif rein.session.query(Document).filter(Document.doc_type == 'enrollment').count() < \
            rein.session.query(User).count():
        click.echo('Continuing previously unfinished setup.')
        get_user(rein, False)
        res = enroll(rein)
        if res['valid']:
            click.echo("Enrollment complete. Run 'rein request' to request free microhosting to sync to.")
            log.info('enrollment complete')
        else:
            click.echo("Signature verification failed. Please try again.")
            log.error('enrollment failed')
    else:
        click.echo("Identity already setup.")
    log.info('exiting setup')


@cli.command()
@click.option('--multi/--no-multi', default=False, help="prompt for identity to use")
@click.option('--identity', type=click.Choice(['Alice', 'Bob', 'Charlie', 'Dan']), default=None, help="identity to use")
def bid(multi, identity):
    """
    Bid on a job.
    """
    log = rein.get_log()
    if multi:
        rein.set_multiuser()

    if rein.has_no_account():
        click.echo("Please run setup.")
        return

    user = get_user(rein, identity)

    key = pubkey(user.dkey)
    url = "http://localhost:5000/"
    click.echo("Querying %s for jobs..." % url)
    sel_url = "{0}query?owner={1}&query=jobs"
    answer = requests.get(url=sel_url.format(url, user.maddr))
    data = answer.json()
    if len(data['jobs']) == 0:
        click.echo('None found')
    jobs = []
    for m in data['jobs']:
        click.echo(m)
        data = verify_sig(m)
        if data['valid']:
            jobs.append(data['info'])
        else:
            click.echo('verify_sig failed')

    job = job_prompt(rein, jobs)
    if not job:
        return
    click.echo("Chosen job: " + str(job))

    log.info('got job for bid')
    res = create_signed_document(rein, "Bid", 'bid',
                                 fields=['user', 'key', 'name', 'amount'],
                                 labels=['Worker\'s name', 'Worker\'s public key', 'Bid name',
                                 'Bid amount (BTC)'], defaults=[user.name, key],
                                 signature_address=user.daddr, signature_key=user.dkey)
    if res:
        click.echo("Bid created. Run 'rein sync' to push to available servers.")
    log.info('bid signed') if res else log.error('bid failed')


@cli.command()
@click.option('--multi/--no-multi', default=False, help="prompt for identity to use")
@click.option('--identity', type=click.Choice(['Alice', 'Bob', 'Charlie', 'Dan']), default=None, help="identity to use")
def post(multi, identity):
    """
    Post a job.
    """
    log = rein.get_log()
    if multi:
        rein.set_multiuser()

    if rein.has_no_account():
        click.echo("Please run setup.")
        return

    user = get_user(rein, identity)

    key = pubkey(user.dkey)
    url = "http://localhost:5000/"
    click.echo("Querying %s for mediators..." % url)
    sel_url = "{0}query?owner={1}&query=mediators"
    answer = requests.get(url=sel_url.format(url, user.maddr))
    data = answer.json()
    if len(data['mediators']) == 0:
        click.echo('None found')
    eligible_mediators = []
    for m in data['mediators']:
        data = verify_sig(m)
        if data['valid']:
            eligible_mediators.append(data['info'])

    mediator = mediator_prompt(rein, eligible_mediators)
    click.echo("Chosen mediator: " + str(mediator))

    log.info('got user and key for post')
    res = create_signed_document(rein, "Job", 'job_posting',
                                 fields=['user', 'key', 'name', 'category', 'description'],
                                 labels=['Job creator\'s name', 'Job creator\'s public key', 'Job name',
                                  'Category', 'Description'], defaults=[user.name, key],
                                 signature_address=user.daddr, signature_key=user.dkey)
    if res:
        click.echo("Posting created. Run 'rein sync' to push to available servers.")
    log.info('posting signed') if res else log.error('posting failed')


@cli.command()
@click.option('--multi/--no-multi', default=False, help="prompt for identity to use")
@click.option('--identity', type=click.Choice(['Alice', 'Bob', 'Charlie', 'Dan']), default=None, help="identity to use")
@click.argument('url', required=True)
def request(multi, identity, url):
    """
    Request free microhosting space
    """
    log = rein.get_log()
    if multi:
        rein.set_multiuser()

    user = get_user(rein, identity)

    if rein.has_no_account():
        click.echo("Please run setup.")
        return

    click.echo("User: " + user.name)
    log.info('got user for request')

    if not url.endswith('/'):
        url = url + '/'
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    create_buckets(rein.engine)

    if get_bucket_count(rein, url) > 4:
        click.echo("You already have enough (5) buckets from %s" % url)
        log.warning('too many buckets')
        return
    sel_url = "{0}request?owner={1}&delegate={2}&contact={3}"

    try:
        answer = requests.get(url=sel_url.format(url, user.maddr, user.daddr, user.contact))
    except:
        click.echo('Error connecting to server.')
        log.error('server connect error')
        return

    if answer.status_code != 200:
        click.echo("Request failed. Please try again later or with a different server.")
        log.error('server returned error')
        return
    else:
        data = json.loads(answer.text)
        click.echo('Success, you have %s buckets at %s' % (str(len(data['buckets'])), url))
        log.info('server request successful')

    if 'result' in data and data['result'] == 'error':
        click.echo('The server returned an error: %s' % data['message'])

    for bucket in data['buckets']:
        b = rein.session.query(Bucket).filter_by(url=url).filter_by(date_created=bucket['created']).first()
        if b is None:
            b = Bucket(url, user.id, bucket['id'], bucket['bytes_free'],
                       datetime.strptime(bucket['created'], '%Y-%m-%d %H:%M:%S'))
            rein.session.add(b)
            rein.session.commit()
        log.info('saved bucket created %s' % bucket['created'])


@cli.command()
@click.option('--multi/--no-multi', default=False, help="prompt for identity to use")
@click.option('--identity', type=click.Choice(['Alice', 'Bob', 'Charlie', 'Dan']), default=None, help="identity to use")
def sync(multi, identity):
    """
    Upload records to each registered server
    """
    log = rein.get_log()
    if multi:
        rein.set_multiuser()

    user = get_user(rein, identity)

    if rein.has_no_account():
        click.echo("Please run setup.")
        return

    click.echo("User: " + user.name)

    create_placements(rein.engine)
    url = "http://localhost:5000/"
    sel_url = url + 'nonce?address={0}'
    answer = requests.get(url=sel_url.format(user.maddr))
    data = answer.json()
    nonce = data['nonce']
    log.info('server returned nonce %s' % nonce)

    check = []
    documents = rein.session.query(Document).filter(Document.identity == user.id).all()
    for doc in documents:
        check.append(doc)
    if len(check) == 0:
        click.echo("Nothing to do.")
    # now that we know what we need to check and upload let's do the checking first, any that
    # come back wrong can be added to the upload queue.
    # download each value (later a hash only with some full downloads for verification)
    upload = []
    verified = []
    for doc in check:
        if len(doc.contents) > 8192:
            click.echo('Document is too big. 8192 bytes should be enough for anyone.')
            log.error("Document oversized %s" % doc.doc_hash)
        else:
            placements = rein.session.query(Placement).filter(and_(Placement.url == url,
                                                                   Placement.doc_id == doc.id)).all()
            if len(placements) == 0:
                upload.append([doc, url])
            else:
                for plc in placements:
                    sel_url = "{0}get?key={1}"
                    answer = requests.get(url=sel_url.format(url, plc.remote_key))
                    data = answer.json()
                    if answer.status_code == 404:
                        log.error("%s not found at %s" % (doc.doc_hash, url))
                        click.echo("document not found")
                        upload.append([doc, url])
                    else:
                        value = data['value']
                        value = value.decode('ascii')
                        value = value.encode('utf8')
                        remote_hash = hashlib.sha256(value).hexdigest()
                        if remote_hash != doc.doc_hash:
                            log.error("%s %s incorrect hash %s != %s " % (url, doc.id, remote_hash, doc.doc_hash))
                            upload.append([doc, url])
                        else:
                            verified.append(doc)

    failed = []
    succeeded = 0
    for doc, url in upload:
        placement = rein.session.query(Placement).filter_by(url=url).filter_by(doc_id=doc.id).all()
        if len(placement) == 0:
            remote_key = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                                 for _ in range(32))
            plc = Placement(doc.id, url, remote_key)
            rein.session.add(plc)
            rein.session.commit()
        else:
            plc = placement[0]
            for p in placement[1:]:
                rein.session.delete(p)
                rein.session.commit()

        if len(doc.contents) > 8192:
            log.error("Document oversized %s" % doc.doc_hash)
            click.echo('Document is too big. 8192 bytes should be enough for anyone.')
        else:
            message = plc.remote_key + doc.contents + user.daddr + nonce
            message = message.decode('utf8')
            message = message.encode('ascii')
            signature = sign(user.dkey, message)
            data = {"key": plc.remote_key,
                    "value": doc.contents,
                    "nonce": nonce,
                    "signature": signature,
                    "signature_address": user.daddr,
                    "owner": user.maddr}
            body = json.dumps(data)
            headers = {'Content-Type': 'application/json'}
            answer = requests.post(url='{0}put'.format(url), headers=headers, data=body)
            res = answer.json()
            if 'result' not in res or res['result'] != 'success':
                log.error('upload failed doc=%s plc=%s url=%s' % (doc.id, plc.id, url))
                failed.append(doc)
            else:
                plc.verified += 1
                rein.session.commit()
                log.info('upload succeeded doc=%s plc=%s url=%s' % (doc.id, plc.id, url))
                click.echo('uploaded %s' % doc.doc_hash)
                succeeded += 1

    sel_url = url + 'nonce?address={0}&clear={1}'
    answer = requests.get(url=sel_url.format(user.maddr, nonce))
    log.info('nonce cleared for %s' % (url))
    click.echo('%s docs checked, %s uploaded.' % (len(check), str(succeeded)))


@cli.command()
def upload():
    """
    Do initial share to many servers.
    """
    servers = ['http://bitcoinexchangerate.org/causeway']
    for server in servers:
        url = '%s%s' % (server, '/info.json')
        text = check_output('curl', url)
        try:
            data = json.loads(text)
        except:
            raise RuntimeError('Problem contacting server %s' % server)

        click.echo('%s - %s BTC' % (server, data['price']))


def get_user(rein, identity):
    if rein.multi and identity:
        rein.user = rein.session.query(User).filter(User.name == identity).first()
    elif rein.multi:
        rein.user = identity_prompt(rein)
    else:
        rein.user = rein.session.query(User).first()
    return rein.user
