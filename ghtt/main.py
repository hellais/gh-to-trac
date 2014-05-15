import github
import argparse

from ghtt.trac import Trac

def parse_args():
    parser = argparse.ArgumentParser(
        description='Tool for converting a github issues to trac tickets')
    parser.add_argument('-s', dest='skip',
                        help='comma separated list of issues to skip')
    parser.add_argument('-r', dest='repo',
                        help='The github repository to migrate')
    parser.add_argument('-u', dest='user',
                        help='The trac username')
    parser.add_argument('-p', dest='password',
                        help='The trac password')
    parser.add_argument('-t', dest='trac',
                        help='The trac repository base url (ex. https://trac.torproject.org/projects/tor)')


    return parser.parse_args()

def list_gh_issues(repo_name, skip):
    gh = github.Github()
    repo = gh.get_repo(repo_name)
    issues = repo.get_issues()
    for issue in issues:
        if int(issue.number) in skip:
            continue
        if issue.state == 'open':
            yield issue
def run():
    args = parse_args()
    skip = map(int, args.skip.split(","))
    trac = Trac(args.trac)
    trac.login(args.user, args.password)
    for issue in list_gh_issues(args.repo, skip):
        print "Migrating issue #%s" % issue.number
        description = "This issue was automatically migrated from github issue "
        description += "https://github.com/%s/issues/%s.\n\n" % (args.repo, issue.number)
        description += issue.body
        trac.create_ticket(issue.title,
                           description, 'Ooni')
