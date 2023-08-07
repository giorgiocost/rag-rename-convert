import os
from PIL import Image
import time
from termcolor import colored
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

# Função para obter a versão incrementada com base nos tipos de commit
def get_incremented_version(commit_messages):
    version_parts = [0, 1, 0]  # Initial version format: major.minor.patch
    for message in commit_messages.values():
        match = re.match(r'^(?P<type>[a-z]+)(?:\((?P<scope>[^\)]+)\))?:(?P<description>.+)$', message)
        if match:
            commit_type = match.group('type')
            if commit_type == 'feat':
                version_parts[1] += 1  # Increment minor version for feature
            elif commit_type == 'fix':
                version_parts[2] += 1  # Increment patch version for fix
            elif commit_type == 'perf':
                version_parts[1] += 1  # Increment minor version for performance improvement
            elif commit_type == 'chore':
                pass  # No version change for chore commits
            # Add more conditions for other types if needed

    return '.'.join(map(str, version_parts))

# Função para gerar o changelog.md
def generate_changelog(new_version):
    commit_messages = get_commit_messages()
    change_log = defaultdict(list)

    for commit_hash, message in commit_messages.items():
        match = re.match(r'^(?P<type>[a-z]+)(?:\((?P<scope>[^\)]+)\))?:(?P<description>.+)$', message)
        if match:
            commit_type = match.group('type')
            commit_scope = match.group('scope') or 'base'
            commit_description = match.group('description')
            commit_date = parse_commit_date(commit_hash)

            change_log[commit_scope].append(f'* {commit_date.strftime("%Y-%m-%d")}: {commit_description}')

    with open('changelog.md', 'w') as changelog_file:
        changelog_file.write(f'## Version {new_version}\n\n')  # Write version at the top
        for scope, changes in change_log.items():
            changelog_file.write(f'### {scope.capitalize()}\n\n')
            changelog_file.write('\n'.join(changes))
            changelog_file.write('\n\n')

# Define o tempo de início
start_time = time.time()

# ... (resto do seu código existente)

# Obtém as mensagens de commit
commit_messages = get_commit_messages()

# Obtém a versão incrementada
new_version = get_incremented_version(commit_messages)

# Gera o changelog.md
generate_changelog(new_version)

print(colored(f'Incremented version to {new_version}', 'light_blue'))

end_time = time.time()
elapsed_time = end_time - start_time
print(colored(f'Script completed successfully in {elapsed_time:.2f} seconds.', 'light_cyan'))
