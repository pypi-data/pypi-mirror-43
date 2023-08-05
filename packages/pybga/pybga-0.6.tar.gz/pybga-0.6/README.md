# ускоряет процесс создания pins в BGA компоненте altium<br/>
<br/>
Описание действий<br/>
-В Altium открываем sch компонента<br/>
-В Altium DXP/Run Script выбираем Import_pins_Altium/ImportPins.PRJSCR(есть в архиве pybga-*.tar.gz)<br/>
-Запускаем RunImportPins<br/>
-Выбираем ./pins_out.csv<br/>
-Нажимаем на Update Mapping<br/>
-Нажимаем Execute и имеем pins для компонента МС<br/>

Как делать  pins_out.csv<br/>
- package_bga.csv(нужно rename to package.csv) содержит пример заполнения входных данных копуса BGA(только des для нужного размера) в виде матрицы BGA корпуса(есть в архиве pybga-*.tar.gz)<br/>
- package_qfp.csv(нужно rename to package.csv) содержит пример заполнения входных данных копуса QFP(только des для нужного размера) в виде одномерной матрицы QFP корпуса(есть в архиве pybga-*.tar.gz)<br/> 
ячейки D2 и Q2(для конктретного значения designator будет своя, у нас Q) должны быть пустыми(без пробелов)<br/>                 
- package_out.csv содержит пример заполнения входных данных копуса(designator и name для нужного размера) в виде матрицы BGA корпуса<br/>
- запускаем функцию pins_bga<br/>
env<br/>
<br/>
from pybga import *<br/>
from pybga import _package<br/>
<br/>
<br/>
<br/>
function: pins_bga(_folder,_dict0,_group0,xs,ys,gs,ggs,holdy,_pack)<br/>
<br/>
_folder -> установим текущую dir где лежит package.csv или package_out.csv и будут другие файлы создаваться:<br/> 
_dict0 -> содержит словарь, который заполнен из datasheet на pins корпуса МС<br/>
_group0 -> содержит список начальных букв имен pins, из которых сформированы группы, расположенные по оси Y<br/>
xs -> стартовая X pins в единицах Altium<br/> 
ys -> стартовая Y pins в единицах Altium<br/>
gs -> расстояние по оси X(в единицах Altium) между двумя соседними группами<br/>  
holdy -> max число pins по оси Y в группе, данный параметр пораждает поддгруппы pins по оси Y, на расстоянии ggs по оси X<br/>
ggs -> расстояние по оси X(в единицах Altium) между подгруппами pins согласно параметру holdy<br/>
output, input -> два файла:<br/>
-package_out.csv это package.csv с заполненными полями<br/>
(создается когда _pack -> _package.PACKAGE_EMPTY )<br/>
(используется как входные данные корпуса когда _pack -> _package.PACKAGE_FILL)<br/>
-cvs out файл pins_out.csv для Import_pins_Altium<br/>
<br/>
 example using(делаем python script):<br/>

from pybga import *<br/>
from pybga import _package<br/>
<br/>
 #dictionary {"des": "name"}<br/>

_dict = {<br/>
"A3": "A0",<br/> 
"B3": "A1",<br/>
"A4": "A2",<br/>
"B4": "A3",<br/>
...<br/>
"M1": "NC"<br/>
}<br/>

_group = {"A","D","Ucc","GND","NC","DP"}<br/>



pins_bga("d:/_temp",_dict,_group,-900,-900,400,100,10,_package.PACKAGE_FILL)<br/>
<br/> 
<br/>
