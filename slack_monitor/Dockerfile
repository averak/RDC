FROM node:12.16-stretch

WORKDIR /app

RUN apt-get update && \
    apt-get install git && \
    apt-get install curl && \
    curl -o- -L https://yarnpkg.com/install.sh | sh

ENV PATH $HOME/.yarn/bin:$HOME/.config/yarn/global/node_modules/.bin:$PATH

