from pyrsistent import PClass, field, PTypeError, InvariantException


__all__ = ['FromConf', 'require', 'field']


_missing = object()
_err_fmt = 'Need exactly one candidate, got {count}{candidates}:{reasons}'
_type_err_fmt = 'Invalid type {actual} for field {field} (expected {expected})'
_missing_err_fmt = 'Missing mandatory field{s} {field}'
_invariant_err_fmt = 'Invariant error{s}: {error}'


def _fmt_reasons(reasons):
    return '\n'.join(
        '  {}.{}\n    - {}\n'.format(
            cls.__module__,
            cls.__name__,
            '\n - '.join(lst),
        )
        for cls, lst in reasons.items()
    )


def _check_requirements(cls, conf):
    conf = dict(conf)
    issues = []
    for name, value in getattr(cls, '__requires', {}).items():
        if name not in conf:
            issues.append('Missing required parameter {}'.format(name))
        else:
            conf_val = conf.pop(name)
            if conf_val != value:
                issues.append('Value {} for parameter {} must be {}'.format(
                    value, name, conf_val,
                ))
    return conf, issues


def require(**requires):
    def _inner(cls):
        cls.__requires = getattr(cls, '__requires', {})
        cls.__requires.update(requires)
        return cls
    return _inner


class FromConf(PClass):
    """Mixin providing from_conf to instantiate appropriate an subclass for a
    given configuration. Uses the field validation logic used in PClass.
    """

    _include_parent = False

    def serialize(self):
        d = super(FromConf, self).serialize()
        d.update(getattr(type(self), '__requires'))
        return d

    @classmethod
    def create(cls, arg):
        if isinstance(arg, cls):
            return arg
        return cls.from_conf(arg)

    @classmethod
    def from_conf(cls, conf=_missing, **kwargs):
        """Instantiates and returns a subclass which is matched by the given
        dict-like conf parameter.
        """
        if kwargs:
            if conf is not _missing:
                kwargs['conf'] = conf
            conf = kwargs
        if cls._include_parent:
            visited = set()
            edge = {cls}
        else:
            visited = {cls}
            edge = set(cls.__subclasses__())
        candidates = set()
        reasons = dict()
        while edge:
            subcls = edge.pop()
            visited.add(subcls)
            edge = (edge | set(subcls.__subclasses__())) - visited
            try:
                new_conf, issues = _check_requirements(subcls, conf)
                if issues:
                    reasons[subcls] = issues
                else:
                    candidates.add(subcls(**new_conf))
            except PTypeError as exc:
                reasons[subcls] = [_type_err_fmt.format(
                    actual=exc.actual_type.__name__,
                    field=exc.field,
                    expected=', '.join(x.__name__ for x in exc.expected_types),
                )]
            except InvariantException as exc:
                reasons[subcls] = []
                if exc.missing_fields:
                    reasons[subcls].append(_missing_err_fmt.format(
                        s='s' if len(exc.missing_fields) > 1 else '',
                        field=', '.join(exc.missing_fields),
                    ))
                if exc.invariant_errors:
                    reasons[subcls].append(_invariant_err_fmt.format(
                        s='s' if len(exc.invariant_errors) > 1 else '',
                        error=', '.join(exc.invariant_errors),
                    ))
            except AttributeError as exc:
                reasons[subcls] = [str(exc)]
        if len(candidates) != 1:
            substr = ', '.join(type(c).__name__ for c in candidates)
            raise ValueError(_err_fmt.format(
                count=len(candidates),
                candidates=' (' + substr + ')' if substr else '',
                reasons='\n' + _fmt_reasons(reasons) if reasons else '',
            ))
        return candidates.pop()
