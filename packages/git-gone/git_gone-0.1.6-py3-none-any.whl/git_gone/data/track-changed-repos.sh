#!/usr/bin/env bash

file="$HOME/.modified";

# Create tracker file if it doesn't exist
if ! [[ -r $file ]]; then
	touch $file;
fi;

track_changed_git_repos()
{
	if git -C "$PWD" rev-parse; then
		# Only append line if doesn't already exist
		if ! $(grep -xq "$PWD" "$file"); then
			echo $PWD >> $file;
		fi;
	fi;
}

chpwd() {
	(track_changed_git_repos >/dev/null 2>&1 &)
}


alias leave="git-gone changes && shutdown now"