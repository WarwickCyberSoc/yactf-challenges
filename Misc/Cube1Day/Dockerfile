#docker build -t cube .

FROM openjdk:16.0.2-jdk-buster

RUN useradd -s /bin/bash wmg
RUN mkdir /server && chown wmg:wmg /server

COPY --chown=wmg:wmg ./server /server

USER wmg
WORKDIR /server

RUN wget https://papermc.io/api/v2/projects/paper/versions/1.17.1/builds/397/downloads/paper-1.17.1-397.jar

EXPOSE 25565

CMD ["java", "-Xms1024M", "-Xmx1024M", "-Dcom.sun.jndi.ldap.object.trustURLCodebase=true", "-Dcom.sun.jndi.rmi.object.trustURLCodebase=true", "-jar", "paper-1.17.1-397.jar"]