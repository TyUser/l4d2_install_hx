Скрипты для быстрого развертывания и управления серверной l4d2 на VDS
===========

<p>Системные требования.</p>

 * 2 ядра процессора;
 * 2 Гб оперативной памяти;
 * Операционная система CentOS 8, Debian 10;


<p>Подготовка к установке на CentOS:</p>

 * yum install epel-release
 * yum update
 * yum install glibc.i686 libstdc++.i686 zlib.i686 screen tar python3 nano
 * firewall-cmd --permanent --add-port=27015/udp
 * adduser game
 * passwd game
 * reboot


<p>Подготовка к установке на Debian:</p>

 * apt update && apt full-upgrade
 * dpkg --add-architecture i386 && apt update && apt install lib32gcc1 lib32stdc++6 lib32z1
 * dpkg --add-architecture amd64 && apt update && apt install screen vsftpd wget
 * adduser game
 * reboot


<p>Установка:</p>

 * su game
 * wget https://www.russerver.com/blog/file/l4d2_install.sh && chmod +x ./l4d2_install.sh
 * ./l4d2_install.sh
 * nano l4d2_cron.py
   > Обязательно изменить ip адрес l4d2 сервера. Переменная sg_ip = '127.0.0.1'
   > 
   > При необходимости изменить port l4d2 сервера. Переменная sg_port = 27015
   > 
   > При необходимости изменить максимальное количество игроков l4d2 сервера. Переменная sg_max_players = 18

 * nano l4d2_restart.py
   > При необходимости изменить port l4d2 сервера. Переменная sg_port = 27015
   > 
   > При необходимости изменить максимальное количество игроков l4d2 сервера. Переменная sg_max_players = 18

<p>Настройка cron на CentOS:</p>

 * su root
 * nano /var/spool/cron/root
 * */2 * * * * su - game -c 'python3 /home/game/l4d2_cron.py' > /dev/null 2>&1
 * 30 6 * * * su - game -c 'python3 /home/game/l4d2_restart.py' > /dev/null 2>&1


<p>Настройка cron на Debian:</p>

 * su root
 * EDITOR='nano'
 * crontab -e
 * */2 * * * * su - game -c 'python3 /home/game/l4d2_cron.py' > /dev/null 2>&1
 * 30 6 * * * su - game -c 'python3 /home/game/l4d2_restart.py' > /dev/null 2>&1


<p>Использование:</p>

 * su game
 * python3 ./l4d2_stop.py
   > Остановить l4d2
 * python3 ./l4d2_restart.py
   > Запустить, перезапустить и автоматическое обновление l4d2


<p>Примечание:</p>

 * Во время своей работы создает лог фаил l4d2.log
 * cron перезапускает сервер в 6:30 каждый день
 * cron раз в 2 минуты проводит опрос l4d2 сервера и если он завис, то принудительно перезагрузит
 * После перезагрузки VDS, сервер l4d2 сам запустится от имени пользователя game
 * Данные скрипты работают на python 3
 * Обязательно настройте правила фаервола
