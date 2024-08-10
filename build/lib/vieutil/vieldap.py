from ldap3 import Server, Connection, ALL
#from expiring_lru_cache import lru_cache, DAYS

#@lru_cache(expires_after=1 * DAYS)
def auth(user, pwd):
    url = 'ldaps://NSDC-ADDC.ad.viemar.automotive'
    domain_user = f'{user}@viemar'
    server = Server(url, get_info=ALL)
    con = Connection(server, user=domain_user, password=pwd, auto_bind=True)
    return con

def get_groups(con, user):
    con.search(
        search_base = 'dc=ad,dc=viemar,dc=automotive',
        #search_scope = SUBTREE,
        search_filter = f'(sAMAccountName={user})',
        attributes = ['memberOf']
    )
    groups_bytes = con.response[0]['raw_attributes']['memberOf']
    groups = []
    for group_bytes in groups_bytes:
        group_full = group_bytes.decode("utf-8")
        group = group_full.split(',')[0].split('=')[1]
        groups.append(group)
    groups_bytes = []
    #print(groups)
    return groups

# exemplo de como usar
if __name__ == '__main__':
    user = 'ftoniolo'
    pwd = 'xxx'
    import time
    start = time.time()
    con = auth(user, pwd)
    end = time.time()
    elapsed = end - start
    print(f'auth time: {elapsed} seconds')
    groups = get_groups(con, user)
    print(groups)
    rpa_prefix = 'rpa_admin'
    rpa_name = 'erp_rpa_analise_pedido_expedicao_variavel_06'
    print(f'{rpa_prefix}_{rpa_name}' in groups)