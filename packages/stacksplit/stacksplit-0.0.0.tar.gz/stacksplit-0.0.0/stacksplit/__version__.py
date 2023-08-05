"""Version of module stacksplit according to PEP 396"""

# may be alpha (a), beta (b), realease candidate (rc) or normal (`empty`)
# plus a number for dev-deploys (eg. 'b0' or 'b1' or 'b2' ...)
APPENDIX = ''

__version_info__ = (0, 0, 0)
__version__ = '.'.join(map(str, __version_info__)) + APPENDIX
