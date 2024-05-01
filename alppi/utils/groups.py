
#!/usr/bin/python
# -*- encoding: utf-8 -*-

SUPERUSER =     'superuser'     ,(100,)
ADMINISTRATOR = 'administrador' ,(100,10)
COORDINATOR =   'coordenador'   ,(100,10,20)
EVALUATOR =     'avaliador'     ,(100,10,20,30)
TEACHER =       'professor'     ,(100,10,20,30,40)
STUDENT =       'estudante'     ,(100,10,20,30,40,50)

GROUPS = {
    'superuser':100,
    'administrador':10,
    'coordenador':20,
    'avaliador':30,
    'professor':40,
    'aluno':50,
}