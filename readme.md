Скрипты для быстрого развертывания и управления серверной l4d2 на VDS
===========

<p>Системные требования.</p>

 * 2 ядра процессора;
 * 2 Гб оперативной памяти;
 * Операционная система CentOS 8;


<p>Подготовка к установке:</p>

 * yum install epel-release
 * yum update
 * yum install glibc.i686 libstdc++.i686 zlib.i686 screen tar python3 nano
 * firewall-cmd --permanent --add-port=27015/udp
 * adduser game
 * passwd game
 * reboot


<p>Установка:</p>

 * su game
 * wget https://www.russerver.com/blog/file/l4d2_install.sh && chmod +x ./l4d2_install.sh
 * ./l4d2_install.sh
 * nano l4d2_cron.py
   > изменить ip адрес l4d2 сервера


<p>Настройка cron:</p>

 * su root
 * nano /var/spool/cron/root
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
