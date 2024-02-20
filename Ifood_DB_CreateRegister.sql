Create table CADASTRO_DB(
Email			varchar(80)        not null,
Telefone		varchar(15)        not null,
Nome            varchar(80)        not null,
id              bigint identity    not null,
endereco        varchar(80)        not null,
num_endereco    varchar(6)         not null,
complemento     varchar(80)        null,
senha           varchar(80)        not null

CONSTRAINT PK_CADASTRO_DB_Email_Id primary key clustered (Email)
)

insert into CADASTRO_DB(Email,Telefone,Nome,endereco,num_endereco,complemento,senha)
values(
'Teste@testemail.com.br',
'11932427543'			,
'Teste da silva junior'	,
'Rua das campinas'		,
'35'					,
'B'						,
'Testedesenha123'
)

insert into CADASTRO_DB(Email,Telefone,Nome,endereco,num_endereco,senha)
values(
'novo@testemail.com.br'			,
'11932427543'					,
'Teste da silva junior'			,
'Rua das campinas'				,
'35'							,
'Testedesenha123'
)

select * from CADASTRO_DB 