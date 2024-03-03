from app.models.counterparty import CounterParty
from app.config.limits_per_client import limits_amina, limits_sygnum


AMINA = CounterParty(name="Amina",
                     id="78766d25-be97-4398-9cc6-f8d58660f172",
                     limits_per_currency=limits_amina)


SYGNUM = CounterParty(name="Sygnum",
                      id="7eee2a7f-7ecb-46ab-a768-c3ec0b502c3f",
                      limits_per_currency=limits_sygnum)



# class AMINA:
#     ID_PREPROD = "ce312f4d-223f-416e-85f0-6ca89d687101"
#     ID_PROD = ""

# class SYGNUM:
#     ID_PREPROD = "2d9dd997-dd0a-40fd-a6db-43c21c82a379"
#     ID_PROD = ""
    

    

