set /p file="Which file do you want to compile? (without the .tex) "
set directory=%cd%
pdflatex -quiet %file%.tex
call C:\ProgramData\Anaconda3\Scripts\activate.bat base
cd C:\Users\DELL\Documents\pythontex-master\pythontex-master\pythontex
python pythontex.py %directory%\%file%.tex
cd %directory%
pdflatex -quiet %file%.tex