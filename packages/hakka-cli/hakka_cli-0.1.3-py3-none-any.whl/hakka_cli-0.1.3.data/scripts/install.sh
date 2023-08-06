#!/usr/bin/env bash

#install brew
if ! type brew &> /dev/null; then
  echo "install brew..."
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
else
  echo "Requirement already satisfied: brew"
fi

#install giter8
if ! type g8 &> /dev/null; then
  echo "install giter 8..."
  brew install giter8
else
  echo "Requirement already satisfied: giter8"
fi
