from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

URL = "mysql+mysqlconnector://root:123456@localhost/ORM_1N_N1"

# $ cd C:\Program Files\MySQL\MySQL Server 8.0\bin
# $ .\mysql.exe -u aluno -p
# mysql> CREATE DATABASE ORM;
# mysql> USE ORM;
# mysql> SHOW TABLES;
Base = declarative_base()


class Cenario(Base):
    __tablename__ = "Cenario"
    id_cenario = Column(Integer, primary_key=True)
    descricao = Column(String(60), nullable=False)

    mapas = relationship("Mapa", backref="cenario")  # envia a chave/id para o Mapa

    def __str__(self):  # Converte dados em string
        return "Cenario(id_cenario={}, descricao=\"{}\")".format(
            self.id_cenario, self.descricao)


class Clima(Base):
    __tablename__ = "Clima"
    id_clima = Column(Integer, primary_key=True)
    descricao = Column(String(60), nullable=False)

    mapas = relationship("Mapa", backref="clima")  # envia a chave/id para o Mapa

    def __str__(self):  # Converte dados em string
        return "Clima(id_clima={}, descricao=\"{}\")".format(
            self.id_clima, self.descricao)


class Inimigo(Base):
    __tablename__ = "Inimigo"
    id_inimigo = Column(Integer, primary_key=True)
    nome_inimigo = Column(String(60))
    hp = Column(Integer, nullable=False)
    experiencia = Column(Integer, nullable=False)

    mapas = relationship("Mapa", backref="inimigo")  # envia a chave/id para o Mapa

    def __str__(self):  # Converte dados em string
        return "Inimigo(id_inimigo={}, nome_inimigo=\"{}\", hp={}, experiencia={})".format(
            self.id_inimigo, self.nome_inimigo, self.hp, self.experiencia)


class Personagem(Base):
    __tablename__ = "Personagem"
    id_personagem = Column(Integer, primary_key=True)
    hp = Column(Integer, nullable=False)
    lv = Column(Integer, nullable=False)
    forca = Column(Integer, nullable=False)
    destreza = Column(Integer, nullable=False)
    classe = Column(String(60))

    jogadores = relationship("Jogador", backref="personagem")  # envia a chave/id para o Jogador

    def __str__(self):  # Converte dados em string
        return "Personagem(id_personagem={}, hp={}, lv={}, forca={}, destreza={}, classe=\"{}\")".format(
            self.id_personagem, self.hp, self.lv, self.forca, self.destreza, self.classe)


class Ranking(Base):
    __tablename__ = "Ranking"
    id_ranking = Column(Integer, primary_key=True)
    pontuacao = Column(Integer, nullable=False)

    jogadores = relationship("Jogador", backref="ranking")  # envia a chave/id para o Jogador

    def __str__(self):  # Converte dados em string
        return "Ranking(id_ranking={}, pontuacao={})".format(
            self.id_ranking, self.pontuacao)

# class Habilidade(Base):
# __tablename__ = "Habilidade"
# id_habilidade = Column(Integer, primary_key=True)
# nomehabilidade = Column(String(60))
# tipo = Column(String(60))

# personagens = relationship("Personagem", backref="habilidade")

# def __str__(self):  # Converte dados em string
# return "Habilidade(id_habilidade={}, nomehabilidade=\"{}\", tipo=\"{}\")".format(
# self.id_habilidade, self.nomehabilidade, self.tipo)


class Jogador(Base):
    __tablename__ = "Jogador"
    id_jogador = Column(Integer, primary_key=True)
    nome = Column(String(150))

    id_personagem = Column(Integer, ForeignKey("Personagem.id_personagem"))  # recebe a chave estrangeira do personagem
    id_ranking = Column(Integer, ForeignKey("Ranking.id_ranking"))  # recebe a chave estrangeira do personagem

    def __str__(self):  # Converte dados em string
        return "Jogador(id_jogador={}, nome=\"{}\")".format(
            self.id_jogador, self.nome)


class Mapa(Base):
    __tablename__ = "Mapa"
    id_mapa = Column(Integer, primary_key=True)
    nome_mapa = Column(String(60))

    id_cenario = Column(Integer, ForeignKey("Cenario.id_cenario"))  # recebe a chave estrangeira do cenario
    id_clima = Column(Integer, ForeignKey("Clima.id_clima"))  # recebe a chave estrangeira do clima
    id_inimigo = Column(Integer, ForeignKey("Inimigo.id_inimigo"))  # recebe a chave estrangeira do inimigo

    def __str__(self):  # Converte dados em string
        return "Mapa(id_mapa={}, nome_mapa=\"{}\")".format(
            self.id_mapa, self.nome_mapa)


def main():
    engine = create_engine(url=URL)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # mysql> DESC Pessoa;

    Session = sessionmaker(engine, expire_on_commit=False)

    # JOGADORES
    # Sessão Personagem
    with Session.begin() as session:
        personagem = Personagem(hp=10, lv=1, forca=10, destreza=10, classe="Depravado")

        for i in range(2):
            personagem.jogadores.append(
                Jogador(nome="Guilherme{}".format(i)))
            # Habilidade(nomehabilidade="LancaDeRaio{}", tipo="Eletrico{}".format(i)))

        session.add(personagem)

    with Session.begin() as session:

        print("============================================")

        personagem = session.query(Personagem).get(1)

        print(personagem)

        for jogador in personagem.jogadores:
            print("   * " + str(jogador))

    # Sessão Ranking
    with Session.begin() as session:
        ranking = Ranking(pontuacao=0)

        for i in range(2):
            ranking.jogadores.append(
                Jogador(nome="Guilherme{}".format(i)))

        session.add(ranking)

    with Session.begin() as session:

        print("============================================")

        ranking = session.query(Ranking).get(1)

        print(ranking)

        for jogador in ranking.jogadores:
            print("   * " + str(jogador))

    # MAPAS
    # Sessão Cenario
    with Session.begin() as session:
        cenario = Cenario(descricao="Consumido pela podridão escarlate")

        for i in range(1):
            cenario.mapas.append(
                Mapa(nome_mapa="Caelid{}".format(i)))

        session.add(cenario)

    # Sessão Clima
    with Session.begin() as session:
        clima = Clima(descricao="chuvoso")

        for i in range(1):
            clima.mapas.append(
                Mapa(nome_mapa="Caelid{}".format(i)))

        session.add(clima)

    with Session.begin() as session:

        print("============================================")

        cenario = session.query(Cenario).get(1)

        print(cenario)

        for mapa in cenario.mapas:
            print("   * " + str(mapa))

    with Session.begin() as session:

        print("============================================")

        clima = session.query(Clima).get(1)

        print(clima)

        for mapa in clima.mapas:
            print("   * " + str(mapa))

        # INIMIGOS
        # Sessão Inimigo
    with Session.begin() as session:
        inimigo = Inimigo(nome_inimigo="Dragao putrido", hp=20, experiencia=150)

        for i in range(1):
            inimigo.mapas.append(
                Mapa(nome_mapa="Caelid{}".format(i)))

        session.add(inimigo)

    with Session.begin() as session:

        print("============================================")

        inimigo = session.query(Inimigo).get(1)

        print(inimigo)

        for mapa in inimigo.mapas:
            print("   * " + str(mapa))

    with Session.begin() as session:

        print("\n================== JOGADOR ==========================")

        jogador = session.query(Jogador).get(1)  # pegando do array um jogador
        mapa = session.query(Mapa).get(1)

        print(jogador)  # printando na tela
        print(jogador.personagem)
        print("\n================== RANKING ==========================")
        print(ranking)
        print("\n==================== MAPA ========================")
        print(mapa)
        print(mapa.cenario)
        print(clima)
        print("\n==================== INIMIGO ========================")
        print(inimigo)
        # print(personagem.habilidade)


if __name__ == "__main__":
    main()
