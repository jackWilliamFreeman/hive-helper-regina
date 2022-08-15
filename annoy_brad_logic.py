import boto3
BRAD_ID = 639967800106024983
TABLE_NAME = 'appData'


session = boto3.Session()
#session = boto3.Session(profile_name='default')
dynamodb = session.resource('dynamodb', region_name="ap-southeast-2")
table = dynamodb.Table(TABLE_NAME)
tables = list(dynamodb.tables.all())

async def annoy_brad(ctx):
    annoyance_payload = get_brad_annoyance_trigger()
    if ctx.author.id == BRAD_ID and annoyance_payload['annoy']:
            await ctx.respond("Fuck off Brad")
            return True
    else: return False

def get_brad_annoyance_trigger():
    response = table.get_item(TableName=TABLE_NAME, Key={'id': 'hive-helper-regina'})
    response_item = response['Item']
    return response_item

async def update_annoyance_trigger(ctx, who, annoy):
    if annoy == 'On':
        ofon = True
    else: ofon = False

    if ctx.author.id != BRAD_ID:
        previous = table.get_item(TableName=TABLE_NAME, Key={'id': 'hive-helper-regina'})
        previous_offender = previous['Item']['annoyer']
        table.put_item(
        Item={
           'id': 'hive-helper-regina',
           'annoy': ofon,
           'annoyer': who,
         })
        await ctx.respond(f"Alright, Brad Annoyance is turned {annoy}, last person to touch it was {previous_offender}")
    else:
        await ctx.respond("Fuck off Brad")