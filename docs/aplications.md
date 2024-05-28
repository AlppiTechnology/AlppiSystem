### step 1
Rodar o banco de dados que cria a network

### step 2
Rodar o Authentication apontando para a mesma network

### step 3
Rodar o System apontando para a mesma network.

#### Configurar o **.env**
- ALLOWED_HOSTS: Colocar o ip da maquina virtual hospedada
- Para DB na mesma instância:
    - DB_HOST_1 = ip do containder do banco (docker inspect)
    - DB_PORT_1 = '14001' porta interna do banco de dado (5432)

[>>> Video Exemple <<<](https://www.youtube.com/watch?v=vJAfq6Ku4cI)