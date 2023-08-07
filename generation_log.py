import os
import re
from collections import defaultdict
from datetime import datetime

# Função para analisar a data de um commit
def parse_commit_date(commit_hash):
    commit_info = os.popen(f'git show -s --format=%ci {commit_hash}').read().strip()
    commit_date = datetime.strptime(commit_info, '%Y-%m-%d %H:%M:%S %z')
    return commit_date

# Função para obter as mensagens de commit
def get_commit_messages():
    commit_log = os.popen('git log --pretty=format:"%H %s"').read().strip().split('\n')
    commit_messages = {}
    
    for line in commit_log:
        commit_hash, message = line.split(' ', 1)
        commit_messages[commit_hash] = message
        
    return commit_messages

# Função para gerar o changelog.md
def generate_changelog():
    commit_messages = get_commit_messages()
    change_log = defaultdict(list)
    
    for commit_hash, message in commit_messages.items():
        match = re.match(r'^(?P<type>[a-z]+)(\((?P<scope>[^\)]+)\))?!?: (?P<description>.+)$', message)
        if match:
            commit_type = match.group('type')
            commit_scope = match.group('scope') or 'base'
            commit_description = match.group('description')
            commit_date = parse_commit_date(commit_hash)
            
            change_log[commit_scope].append(f'* {commit_date.strftime("%Y-%m-%d")}: {commit_description}')
    
    with open('changelog.md', 'w') as changelog_file:
        for scope, changes in change_log.items():
            changelog_file.write(f'## {scope.capitalize()}\n\n')
            changelog_file.write('\n'.join(changes))
            changelog_file.write('\n\n')

# Gera o changelog.md
generate_changelog()
