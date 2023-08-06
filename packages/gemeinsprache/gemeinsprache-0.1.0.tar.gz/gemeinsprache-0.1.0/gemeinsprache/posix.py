#!/usr/bin/env python
import os
import stat
import pwd
import sys


class PosixFilepath:
    def __init__(self, user, path, curr_dir=None):
        
        prev_dir = os.getcwd()
        if curr_dir:
            os.chdir(curr_dir)
        self.exists = os.path.exists(path)
        self.path = path
        self.user = user
        self.realpath = os.path.realpath(os.path.expanduser(path))
        self.abspath = os.path.abspath(self.realpath)
        self.is_file = os.path.isfile(path)
        self.is_dir = os.path.isdir(path)
        self.is_symlink = os.path.islink(path)
        self.stat = os.stat(self.abspath)
        self.user_id, self.group_id = pwd.getpwnam(user).pw_uid, pwd.getpwnam(user).pw_gid
        self.mode = self.stat[stat.ST_MODE]
        self.is_owner = self.user_id == self.stat[stat.ST_UID]
        self.is_group = self.group_id == self.stat[stat.ST_UID]
        self.is_orphaned = self.stat.S_IRWXO & self.mode == stat.S_IRWXO
        self.has_owner_rwx = self.is_owner & self.stat.S_IRWXU & self.mode  == self.stat.S_IRWXU
        self.has_group_rwx = self.is_group & self.stat.S_IRWXG & self.mode == stat.S_IRWXG
        self.has_world_rwx = self.stat.S_IRWXO & self.mode == stat.S_IRWXO
        self.has_rwx = self.has_owner_rwx or self.has_group_rwx or self.has_world_rwx
        self.credentials = 'owner' if self.has_owner_rwx else 'group' if self.has_group_rwx else 'world' if self.has_world_rwx else ''
        if curr_dir:
            os.chdir(prev_dir)

class PosixDirectory(PosixFilepath):
    def __init__(self, user, path, curr_dir=None):
        super().__init__(user, path, curr_dir)
        if not self.is_dir:
            raise ValueError(f"Not a directory: {path}")
    def ls(self):
        for fp in os.listdir(self.abspath):
            print(os.path.abspath(fp))


