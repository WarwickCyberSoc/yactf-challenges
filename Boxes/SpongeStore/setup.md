This is a rough guide on setting up this box:

Configure VM with `peter:peter` initially.
Add user `angus:angus`.
```
echo """
Hey Angus,

We seem to be getting some TCP fragmentation issues on this machine, not sure why exactly.

Could you get some packet dumps made and we'll review them at the next team meeting?

Thanks,
Peter
""" > /home/angus/todo.txt
chown root:angus /home/angus/todo.txt
chmod 440 /home/angus/todo.txt
chattr +i /home/angus/todo.txt
rm /home/angus/.bash_history && ln -s /dev/null /home/angus/.bash_history
```

Setup /etc/hosts:
`echo 'spongestore.wmg 127.0.0.1' >> /etc/hosts`

Setup flags:
```
echo 'WMG{goOd_OL_UN4U7H3N7ic473d_rc3_7HrOUgh_WorDPr355_pLUgIn2}' > /home/angus/flag.txt
chown root:angus /home/angus/flag.txt
chmod 440 /home/angus/flag.txt
chattr +i /home/angus/flag.txt

echo 'WMG{w417_1_5h0ULDn7_l37_P30pl3_5ud0_r4nD0m_Pr09r4mZ??}' > /root/flag.txt
chown root:root /root/flag.txt
chmod 440 /root/flag.txt
chattr +i /root/flag.txt
```

```
rm /home/peter/.bash_history && ln -s /dev/null /home/peter/.bash_history
```
# Wordpress
Install Wordpress:
```
sudo apt update
sudo apt install apache2 \
                 ghostscript \
                 libapache2-mod-php \
                 mysql-server \
                 php \
                 php-bcmath \
                 php-curl \
                 php-imagick \
                 php-intl \
                 php-json \
                 php-mbstring \
                 php-mysql \
                 php-xml \
                 php-zip
```
Unzip wordpress.zip in repo

Follow https://ubuntu.com/tutorials/install-and-configure-wordpress#5-configure-database to setup mySQL

Use following password:
`CREATE USER wordpress@localhost IDENTIFIED BY 'C8AzLSKhbf&nkCDy';`

# User:
```
CREATE DATABASE stockcheck;
CREATE USER stockcheck@localhost IDENTIFIED BY '57r0n6357_club_0n_c4mpu5';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP,ALTER ON stockcheck.* TO stockcheck@localhost;
FLUSH PRIVILEGES;
```

```
USE stockcheck;
CREATE TABLE `stock` (
	`id` VARCHAR(32) NOT NULL,
	`name` VARCHAR(256),
	`last_updated` DATE,
	`in_stock` INT,
	`on_backorder` INT,
	`archived` INT,
	PRIMARY KEY (`id`)
);
INSERT INTO stock (id, name, last_updated, in_stock, on_backorder, archived) VALUES
("SPP001", "Yellow Sponge", "2022-01-05", 431511, 120000, 0),
("SPP002", "Green Sponge", "2022-01-05", 62622, 50000, 0),
("SPP003", "Pink Sponge", "2022-01-05", 12389, 65000, 0),
("SPPA001", "Abrasive Yellow Sponge", "2022-01-05", 12112, 95000, 0),
("SPPA002", "Abrasive Green Sponge", "2022-01-05", 83111, 32500, 0),
("SPPA003", "Abrasive Pink Sponge", "2022-01-05", 32541, 9000, 0);

```

```
sudo apt-get install libmysqlclient-dev python3-pip
pip install flask flask_mysqldb
```

```
chown -R root:angus /home/angus/stockchecker 
find /home/angus/stockchecker -type d -exec chmod 750 {} +
find /home/angus/stockchecker -type f -exec chmod 640 {} +
```

# Root:
```apt install tshark```

Add to `/etc/sudoers`:
```
angus ALL=(ALL:ALL) /usr/bin/tshark
``` 

# Scripts
Put `cleanup.sh` in /root/.cleanup
Put `cleanup.service`, `cleanup.timer`, `stockchecker.service` in `/etc/systemd/system`

Then enable them and start:
```
systemctl daemon-reload
systemctl enable cleanup.timer && systemctl start cleanup.timer
systemctl enable cleanup.service
systemctl enable stockchecker.service && systemctl start stockchecker.service
```

# Finally
Used creds: 
```
Users:

peter:mnXhfg7zq@GX@KC$
angus:57r0n6357_club_0n_c4mpu5

Databases:
wordpress:C8AzLSKhbf&nkCDy
stockcheck:57r0n6357_club_0n_c4mpu5

Wordpress:
peter:1#d1$N*ftytt7aU(zc

```