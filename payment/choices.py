"""Payment Choices"""


card_type_choices = (
    ('unknown', 'UNKNOWN'),
	('verve', 'VERVE'),
    ('mastercard', 'MASTERCARD')
)

DEFAULT_CARD_TYPE = 'unknown'

DEFAULT_TRANSACTION_TYPE = 'ORDER'


countries_to_currencies = {
	'nigeria': 'NGN'
}