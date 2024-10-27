from bet_maker.schemas.incoming import Bet
from decimal import Decimal


create_bet_request = Bet(bid=Decimal("10.11"), event_id=1).model_dump_json()
