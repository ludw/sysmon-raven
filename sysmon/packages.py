import pkg_resources
from pkg_resources import parse_version, Requirement
from setuptools import package_index

pi = package_index.PackageIndex()


def get_installed():
    working_set = pkg_resources.working_set
    versions = dict([(d.key, d.version) for d in working_set])
    return sorted(versions.items())


def normalize_version(parsed_version):
    normalized = []
    for part in parsed_version:
        if not part.startswith('*'):
            normalized.append(int(part))
        else:
            if part.startswith('*@'):
                normalized.append(-1)
    while len(normalized) < 3:
        normalized.append(0)
    return normalized


def find_latest(current_version, versions):
    current_version_norm = normalize_version(parse_version(current_version))
    newest = current_version_norm, current_version
    newest_major = current_version_norm, current_version
    newest_minor = current_version_norm, current_version

    for version in versions:
        dist_version = normalize_version(parse_version(version))

        if dist_version[0] == newest_minor[0][0]:
            if dist_version[1] == newest_minor[0][1]:
                if dist_version[2] > newest_minor[0][2]:
                    newest_minor = dist_version, version

        if dist_version[0] == newest_major[0][0]:
            if dist_version[1] == newest_major[0][1]:
                if dist_version[2] > newest_major[0][2]:
                    newest_major = dist_version, version
            if dist_version[1] > newest_major[0][1]:
                newest_major = dist_version, version

        if dist_version[0] == newest[0][0]:
            if dist_version[1] == newest[0][1]:
                if dist_version[2] > newest[0][2]:
                    newest = dist_version, version
            if dist_version[1] > newest[0][1]:
                newest = dist_version, version
        if dist_version[0] > newest[0][0]:
            newest = dist_version, version

    return current_version, newest[1], newest_major[1], newest_minor[1]


def get_latest(name, current_version):
    req = Requirement.parse(name)
    pi.find_packages(req)
    versions = [x.version for x in pi[req.key]]

    return find_latest(current_version, versions)


def check_version(name, current_version):
    current, newest, newest_major, newest_minor = get_latest(name, current_version)
    print "Current version of {name}: {v}".format(name=name, v=current_version)
    if current != newest_minor:
        print "Newer minor version of {name}: {v}".format(name=name, v=newest_minor)

    if current != newest_major:
        print "Newer major version of {name}: {v}".format(name=name, v=newest_major)

    if current != newest:
        print "Newest version of {name}: {v}".format(name=name, v=newest)

if __name__ == "__main__":
    for name, current_version in get_installed():
        check_version(name, current_version)
