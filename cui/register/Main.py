#!/usr/bin/python3
#!python3
#encoding:utf-8
import os.path
import subprocess
import dataset
import database.src.Database
import database.src.account.Main
import cui.register.github.api.v3.authorizations.Authorizations
import web.sqlite.Json2Sqlite
class Main:
    def __init__(self, path_dir_db):
        self.path_dir_db = path_dir_db
        self.j2s = web.sqlite.Json2Sqlite.Json2Sqlite()

    def Insert(self, args):
        print('Account.Insert')
        print(args)
        print('-u: {0}'.format(args.username))
        print('-p: {0}'.format(args.password))
        print('-m: {0}'.format(args.mailaddress))
        print('-s: {0}'.format(args.ssh_public_key_file_path))
        print('-t: {0}'.format(args.two_factor_secret_key))
        print('-r: {0}'.format(args.two_factor_recovery_code_file_path))
        print('--auto: {0}'.format(args.auto))

        db = database.src.Database.Database()
        db.Initialize()
        
        print(db.account['Accounts'].find_one(Username=args.username))
        if None is db.account['Accounts'].find_one(Username=args.username):
            print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
            # 1. APIでメールアドレスを習得する。https://developer.github.com/v3/users/emails/
            # 2. Tokenの新規作成
            auth = cui.register.github.api.v3.authorizations.Authorizations.Authorizations(args.username, args.password)
            token_repo = auth.Create(args.username, args.password, scopes=['repo'])
            token_delete_repo = auth.Create(args.username, args.password, scopes=['delete_repo'])
            token_user = auth.Create(args.username, args.password, scopes=['user'])
            token_public_key = auth.Create(args.username, args.password, scopes=['admin:public_key'])
            # 3. SSH鍵の新規作成
            # 4. 全部成功したらDBにアカウントを登録する
#            args.mailaddress = APIで取得する
            db.account['Accounts'].insert(self.__CreateRecordAccount(args))
            account = db.account['Accounts'].find_one(Username=args.username)
            if None is not args.two_factor_secret_key:
                db.account['AccessTokens'].insert(self.__CreateRecordTwoFactor(account['Id'], args))
            db.account['AccessTokens'].insert(self.__CreateRecordToken(account['Id'], token_repo))
            db.account['AccessTokens'].insert(self.__CreateRecordToken(account['Id'], token_delete_repo))
            db.account['AccessTokens'].insert(self.__CreateRecordToken(account['Id'], token_user))
            db.account['AccessTokens'].insert(self.__CreateRecordToken(account['Id'], token_public_key))

        # 作成したアカウントのリポジトリDB作成や、作成にTokenが必要なライセンスDBの作成
        db.Initialize()
        return db

    def __CreateRecordAccount(self, args):
        return dict(
            Username=args.username,
            MailAddress=args.mailaddress,
            Password=args.password,
            CreateAt="1970-01-01T00:00:00Z"
        )
        # 作成日時はAPIのuser情報取得によって得られる。
        
    def __CreateRecordToken(self, account_id, j):
        return dict(
            AccountId=account_id,
            IdOnGitHub=j['id'],
            Note=j['note'],
            AccessToken=j['token'],
            Scopes=self.j2s.ArrayToString(j['scopes'])
        )

    def __CreateRecordTwoFactor(self, account_id, args):
        return dict(
            AccountId=account_id,
            Secret=args.args.two_factor_secret_key
        )
    """    
    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
    """
    """
        # アカウントDBが存在しないなら作成する
        path_db_account = os.path.join(self.path_dir_db, 'GitHub.Accounts.sqlite3')
        if not(os.path.isfile(path_db_account)):
            db = database.src.account.Main.Main(self.path_dir_db)
            db.Create()
        db_account = dataset.connect('sqlite:///' + path_db_account)
        print(path_db_account)

        # DBから探す。指定ユーザ名のアカウントが存在するか否かを。
        account = db_account['Accounts'].find_one(Username=args.username)
        auth = cui.register.github.api.v3.authorizations.Authorizations.Authorizations(args.username, args.password)
        auth.Create(args.username, args.password, scopes=['public_repo'])
        if None is account:
            auth = cui.register.github.api.v3.authorizations.Authorizations.Authorizations(args.username, args.password)
            # 1. APIでメールアドレスを習得する。https://developer.github.com/v3/users/emails/
            # 2. Tokenの新規作成
            auth.Create(scopes=['public_repo'])
            auth.Create(scopes=['delete_repo'])
            auth.Create(scopes=['read:public_key'])
            auth.Create(scopes=['write:public_key'])
            # user(read:user, user:email, user:follow)
            # repo(repo:status, repo_deployment, public_repo)
#            auth.Create(args.username, args.password, scopes=['user:email'])
#            auth.Create(args.username, args.password, scopes=['repo'])
#            auth.Create(args.username, args.password, scopes=['repo', 'public_repo'])
#            auth.Create(args.username, args.password, scopes=['admin:public_key', 'read:public_key'])
#            auth.Create(args.username, args.password, scopes=['admin:public_key', 'write:public_key'])
            # 3. SSH鍵の新規作成
            # 4. 全部成功したらDBにアカウントを登録する        

        # アカウントDBにレコードが1つでもある。かつ、ライセンスDBが存在しないなら
        # * LicenseマスターDB作成
        
        # 各ユーザのリポジトリDB作成
        for account in db_account['Accounts'].find():
            # まだ該当ユーザのリポジトリDBが存在しないなら作成する
            pass

        # * Otherリポジトリは作成しなくていい。今のところ使わないから。
        """
        
    def Update(self, args):
        print('Account.Update')
        print(args)
        print('-u: {0}'.format(args.username))
        print('-p: {0}'.format(args.password))
        print('-m: {0}'.format(args.mailaddress))
        print('-s: {0}'.format(args.ssh_public_key_file_path))
        print('-t: {0}'.format(args.two_factor_secret_key))
        print('-r: {0}'.format(args.two_factor_recovery_code_file_path))
        print('--auto: {0}'.format(args.auto))

    def Delete(self, args):
        print('Account.Delete')
        print(args)
        print('-u: {0}'.format(args.username))
        print('--auto: {0}'.format(args.auto))

    def Tsv(self, args):
        print('Account.Tsv')
        print(args)
        print('path_file_tsv: {0}'.format(args.path_file_tsv))
        print('--method: {0}'.format(args.method))

