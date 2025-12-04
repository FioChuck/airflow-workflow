PYTHON_VERSION="3.11.10" # run pyenv install -l to see all versions available in pyenv
# ex: openjdk-8-jdk, openjdk-11-jdk, openjdk-17-jdk, etc.


rm -fr ~/.pyenv
curl -fsSL https://pyenv.run | bash

grep -q "PYENV_ROOT" ~/.bashrc || {

	cat <<'EOT' | tee -a ~/.bashrc ~/.profile ~/.bash_profile >/dev/null

# --- Pyenv Environment Variables ---
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"
source ~/.bashrc
EOT
}

# #  run for current session
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - bash)"
eval "$(pyenv virtualenv-init -)"

sudo apt update
sudo apt install -y make build-essential libssl-dev zlib1g-dev \
	libbz2-dev libreadline-dev libsqlite3-dev curl git \
	libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev

pyenv install $PYTHON_VERSION

pyenv virtualenv $PYTHON_VERSION composer_env
pyenv local composer_env
