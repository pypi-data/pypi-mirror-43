from .ldap import parse_scope
from .role import RoleOptions
from .utils import string_types
from .utils import iter_format_fields

default_ldap_query = {
    'base': '',
    'filter': '(objectClass=*)',
    'scope': 'sub',
}


def ldapquery(value):
    if not isinstance(value, dict):
        raise ValueError("ldap: is not a dict")

    query = dict(default_ldap_query, **value)
    query['scope'] = parse_scope(query['scope'])
    if 'filter' in query:
        query['filter'] = query['filter'].rstrip('\r\n')

    # Clean value from old manual attribute
    query.pop('attribute', None)

    return query


def privilege(raw):
    allowed_keys = set(['grant', 'inspect', 'revoke', 'type'])
    defined_keys = set(raw.keys())
    spurious_keys = defined_keys - allowed_keys

    if spurious_keys:
        msg = "Unknown keys %s" % (', '.join(spurious_keys),)
        raise ValueError(msg)

    raw.setdefault('type', 'nspacl')

    return raw


def privileges(raw):
    if not isinstance(raw, dict):
        raise ValueError('privileges must be a dict')

    value = {}
    for k, v in raw.items():
        if isinstance(v, list):
            value[k] = v
        elif isinstance(v, dict):
            value[k] = privilege(v)
        else:
            msg = "Unknown value %.32s for %s" % (v, k,)
            raise ValueError(msg)
    return value


def rolerule(value):
    rule = value

    if value is None:
        raise ValueError("Empty role rule. Wrong indentation?")

    if isinstance(rule, string_types):
        rule = dict(names=[rule])

    strlist_alias(rule, 'names', 'name')
    compat_ldap_attribute(rule, 'name')
    if 'names' not in rule:
        raise ValueError("Missing role name")

    strlist_alias(rule, 'parents', 'parent')
    compat_ldap_attribute(rule, 'parent')
    rule.setdefault('parents', [])

    strlist_alias(rule, 'members', 'member')
    compat_ldap_attribute(rule, 'member')
    rule.setdefault('members', [])

    options = rule.setdefault('options', {})

    if isinstance(options, string_types):
        options = options.split()

    if isinstance(options, list):
        options = dict(
            (o[2:] if o.startswith('NO') else o, not o.startswith('NO'))
            for o in options
        )

    rule['options'] = RoleOptions(**options)
    rule.setdefault('on_unexpected_dn', 'fail')
    return rule


def alias(dict_, key, alias, default=None):
    if alias in dict_:
        dict_.setdefault(key, dict_.pop(alias, default))


def strorlist(dict_, key, exceptions=[]):
    if key in dict_:
        v = dict_[key]
        if v not in exceptions and isinstance(v, string_types):
            dict_[key] = [v]
        return dict_[key]


def strlist_alias(dict_, key, alias_, exceptions=[]):
    alias(dict_, key, alias_)
    return strorlist(dict_, key, exceptions)


def compat_ldap_attribute(rule, name):
    name_attribute = name + '_attribute'
    names = name + 's'
    if name_attribute in rule:
        value = rule.get(names, [])
        rule[names] = value + ['{%s}' % rule.pop(name_attribute)]


def grantrule(value, defaultdb='__all__', defaultschema='__all__'):
    if not isinstance(value, dict):
        raise ValueError('Grant rule must be a dict.')

    alias(value, 'privilege', 'acl')
    compat_ldap_attribute(value, 'role')
    strlist_alias(value, 'roles', 'role')

    value.setdefault('database', defaultdb)
    strlist_alias(value, 'databases', 'database', ['__all__'])

    value.setdefault('schema', defaultschema)
    strlist_alias(value, 'schemas', 'schema', [None, '__any__', '__all__'])

    if 'privilege' not in value:
        raise ValueError('Missing privilege to grant rule.')

    allowed_keys = set([
        'privilege', 'databases', 'schemas',
        'roles', 'role_match',
    ])
    defined_keys = set(value.keys())

    if defined_keys - allowed_keys:
        msg = 'Unknown parameter to grant rules: %s' % (
            ', '.join(defined_keys - allowed_keys)
        )
        raise ValueError(msg)

    if 'roles' not in value:
        raise ValueError('Missing role in grant rule.')

    return value


def ismapping(value):
    # Check whether a YAML value is supposed to be a single mapping.
    if not isinstance(value, dict):
        return False
    return bool(set(['grant', 'ldap', 'role', 'roles']) >= set(value.keys()))


def iter_mapping_strings(mapping):
    for role in mapping.get('roles', []) + mapping.get('grant', []):
        for k, v in role.items():
            if not isinstance(v, list):
                v = [v]
            for v1 in v:
                if hasattr(v1, 'splitlines'):
                    yield v1


def mapping(value, **kw):
    # A single mapping from a query to a set of role rules. This function
    # translate random YAML to cannonical schema.

    if not isinstance(value, dict):
        raise ValueError("Mapping should be a dict.")

    if 'role' in value:
        value['roles'] = value.pop('role')
    if 'roles' not in value:
        value['roles'] = []
    if not isinstance(value['roles'], list):
        value['roles'] = [value['roles']]

    value['roles'] = [rolerule(r) for r in value['roles']]

    if 'grant' in value:
        if isinstance(value['grant'], dict):
            value['grant'] = [value['grant']]
        value['grant'] = [grantrule(g, **kw) for g in value['grant']]

    if not value['roles'] and 'grant' not in value:
        # Don't accept unused LDAP queries.
        raise ValueError("Missing role or grant rule.")

    if 'ldap' in value:
        value['ldap'] = ldapquery(value['ldap'])
        strings = iter_mapping_strings(value)
        attrs = set(iter_format_fields(strings, split=True))
        if 'dn' in attrs:
            attrs.remove('dn')
        if not attrs:
            fmt = "No attributes are used from LDAP query %(base)s"
            raise ValueError(fmt % value['ldap'])
        value['ldap']['attributes'] = list(attrs)

    return value


def _flatten_legacy_map(value):
    for dbname, dbvalue in value.items():
        if ismapping(dbvalue):
            dbvalue = [dbvalue]

        if isinstance(dbvalue, dict):
            for schema, svalues in dbvalue.items():
                if ismapping(svalues):
                    svalues = [svalues]
                for svalue in svalues:
                    yield mapping(
                        svalue, defaultdb=dbname, defaultschema=schema)
        elif isinstance(dbvalue, list):
            for v in dbvalue:
                yield mapping(v, defaultdb=dbname)


def syncmap(value):
    # Validate and translate raw YAML value to cannonical form used internally.
    #
    # A sync map has the following canonical schema:
    #
    #   - ldap: <ldapquery>
    #     roles:
    #     - <rolerule>
    #     - ...
    #     grant:
    #     - <grantrule>
    #     - ...
    #   ...
    # ...
    #
    # But we accept a wide variety of shorthand schemas:
    #
    # Single mapping:
    #
    # roles: [<rolerule>]
    #
    # List of mapping:
    #
    # - roles: [<rolerule>]
    # - ...
    #
    # dict of dbname->single mapping (legacy)
    #
    # appdb:
    #   roles: <rolerule>
    #
    # dict of dbname->list of mapping (legacy)
    #
    # appdb:
    # - roles: <rolerule>
    #
    # dict of dbname->schema->single mapping (legacy)
    #
    # appdb:
    # - roles: <rolerule>
    # dict of dbname->schema->single mapping (legacy)
    #
    # appdb:
    #   appschema:
    #     roles: <rolerule>

    if not value:
        return []

    if ismapping(value):
        value = [value]

    if isinstance(value, list):
        return [mapping(v) for v in value]
    elif isinstance(value, dict):
        return list(_flatten_legacy_map(value))
    else:
        raise ValueError("Illegal value for sync_map.")


def raw(v):
    return v


def shared_queries(v):
    if not v:
        return {}
    if not hasattr(v, 'items'):
        raise ValueError("shared_queries must be dict.")
    for k, q in v.items():
        if not isinstance(q, string_types):
            raise ValueError("Bad query %s." % k)
    return v


VERBOSITIES = [
    'CRITICAL',
    'ERROR',
    'WARNING',
    'CHANGE',
    'INFO',
    'DEBUG',
]


def verbosity(v):
    if isinstance(v, list):
        v = sum(v)
        v = max(0, v)
        v = min(v, 5)
        v = VERBOSITIES[v]

    if v not in VERBOSITIES:
        raise ValueError("Unknown verbosity '%s'" % (v,))

    return v
