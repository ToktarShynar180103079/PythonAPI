import os
import sys
from io import StringIO

AuthorInf = {'Name' : 'Bogdanchikov Andrey', 'Email' : 'andrey.bogdanchikov@sdu.edu.kz', 'Position':'Associate Professor in Computer Sciences Department', 'Affilation':'Suleyman Demirel University'}
PubList = [{'Site': 'Scopus', 'Authors': 'Kangozhin, B. R.;Baimuratov, O. A.;Zharmagambetova, M. S.;Dautov, S. S.;Kangozhin, D. B.', 'Title': 'Noise Immunity of Devices of Automated Systems for Technological Control of Energy Facilities in the Almaty Region', 'Type': 'Book Chapter', 'Link': None, 'Year': '2022', 'Where published': 'Studies in Systems, Decision and Control', 'PP.': '277-290', 'Volume': '399', 'KeyWords': 'Aggregated interference | Automated process of control systems | Electrical substation | Electromagnetic compatibility | Electromagnetic environment | Electromagnetic interference | Grounding device | Radiated pulse interference | Relay protection and automation'},
           {'Site': 'Scopus', 'Authors': 'Aitchanov, Bekmurza;Baimuratov, Olimzhon;Zhussupekov, Muratbek;Aitzhanov, Tleu', 'Title': 'Contact Centers Management Models: Analysis and Recommendations', 'Type': 'Conference Paper', 'Link': None, 'Year': '28 April 2021', 'Where published': 'SIST 2021 - 2021 IEEE International Conference on Smart Information Systems and Technologies', 'PP.': None, 'Volume': None, 'KeyWords': 'Call Center | Contact Center | IT company | IT management | IT management models | IT service efficiency | operational cycle'},
           {'Site': 'Scopus', 'Authors': 'Tulemissova, Gulfarida;Baimuratov, Olimzhon', 'Title': 'Review of Electronic Industry in Kazakhstan: Conditions and Opportunities', 'Type': 'Conference Paper', 'Link': None, 'Year': '2021', 'Where published': 'Proceedings - 2021 16th International Conference on Electronics Computer and Computation, ICECCO 2021', 'PP.': None, 'Volume': None, 'KeyWords': 'Electronics industry | EMS industry | Fabless manufacturing | FinFET technology | Information technology industry'},
           {'Site': 'Scopus', 'Authors': 'Kuanyshbay, Darkhan;Baimuratov, Olimzhon;Amirgaliyev, Yedilkhan;Kuanyshbayeva, Arailym', 'Title': 'Speech data collection system for Kazakh language', 'Type': 'Conference Paper', 'Link': None, 'Year': '2021', 'Where published': 'Proceedings - 2021 16th International Conference on Electronics Computer and Computation, ICECCO 2021', 'PP.': None, 'Volume': None, 'KeyWords': 'audio | automatic speech recognition | dataset | recording'},
           {'Site': 'Scopus', 'Authors': 'Aitchanov, Bekmurza;Baimuratov, Olimzhon;Zhussupekov, Muratbek;Aitchanov, Tley', 'Title': 'Analysis of Key Elements for Modern Contact Center Systems to Improve Quality', 'Type': 'Book Chapter', 'Link': None, 'Year': '2021', 'Where published': 'Lecture Notes on Data Engineering and Communications Technologies', 'PP.': '162-174', 'Volume': '83', 'KeyWords': 'Contact center | Object-oriented organizational model | Organizational model | Organizational processes | Resource accounting | Resource management'},
           {'Site': 'Scopus', 'Authors': 'Tulemissova, Gulfarida;Baimuratov, Olimzhon', 'Title': 'Cyber security system of FPGA platform for wireless sensor networks', 'Type': 'Conference Paper', 'Link': None, 'Year': '2020', 'Where published': 'European Conference on Information Warfare and Security, ECCWS', 'PP.': '351-361', 'Volume': '2020-June', 'KeyWords': 'FPGA bit stream algorithms; clustering intrusion detection methods | Information security | Machine learning | Multi-agent system | Wireless sensor network (WSN)'},
           {'Site': 'Scopus', 'Authors': 'Aziza, Aipenova;Araily, Khuandykh;Olimzhon, Baimuratov', 'Title': 'The analysis of indexes quality of a healthcare in Kazakhstan', 'Type': 'Conference Paper', 'Link': None, 'Year': '4 February 2019', 'Where published': '14th International Conference on Electronics Computer and Computation, ICECCO 2018', 'PP.': None, 'Volume': None, 'KeyWords': 'Healthcare development | Medical services | Quality of medical services'},
           {'Site': 'Scopus', 'Authors': 'Aitchanov, B. Kh;Baimuratov, O. A.;Aldibekova, A. N.', 'Title': 'Development of the system with NMR based on electromagnetic coils for milk processing', 'Type': 'Conference Paper', 'Link': None, 'Year': '4 February 2019', 'Where published': '14th International Conference on Electronics Computer and Computation, ICECCO 2018', 'PP.': None, 'Volume': None, 'KeyWords': 'Changing the properties of milk | Control system | Improving the quality of milk | Magnetic treatment | Quality control of milk | The stabilization of the magnetic field'},
           {'Site': 'Scopus', 'Authors': 'Aitimov, M. Zh;Ozhikenov, K. A.;Aitimova, U. Zh;Dauitbayeva, A. O.;Baimuratov, O. A.', 'Title': 'Analysis of the structure and calculation of time for the environmental monitoring system with multi-parameter sensors', 'Type': 'Article', 'Link': None, 'Year': '2017', 'Where published': 'News of the National Academy of Sciences of the Republic of Kazakhstan, Series of Geology and Technical Sciences', 'PP.': '149-156', 'Volume': '2', 'KeyWords': 'Control | Environment | Monitoring | Multifunctional sensors'},
           {'Site': 'Scopus', 'Authors': 'Mukhanov, Bakhyt;Omirbekova, Zhanar;Alimanova, Madina;Jumadilova, Shynara;Kozhamzharova, Dinara;Baimuratov, Olimzhon', 'Title': 'A model of virtual training application for simulation of technological processes', 'Type': 'Conference Paper', 'Link': None, 'Year': '2015', 'Where published': 'Procedia Computer Science', 'PP.': '177-182', 'Volume': '56', 'KeyWords': 'Control system | Human-machine interface | In situ leaching | Simulation of technological processes | Supervisory Control and Data Acquisition (SCADA) | Virtual training application | Web applications | Workflow'},
           {'Site': 'Scopus', 'Authors': 'Kuandykov, Abu;Uskenbayeva, Raissa;Cho, Young Im;Kozhamzharova, Dinara;Baimuratov, Olimzhon;Chinibayev, Yersain;Karimzhan, Nurlan', 'Title': 'Multi-agent based anti-locust territory protection system', 'Type': 'Conference Paper', 'Link': None, 'Year': '2015', 'Where published': 'Procedia Computer Science', 'PP.': '477-483', 'Volume': '56', 'KeyWords': 'Agent based modeling | HARMS | Heterogeneous robots | Locust control'},
           {'Site': 'Scopus', 'Authors': 'Kuandykov, A. A.;Uskenbayeva, R. K.;Cho, Y. I.;Kozhamzharova, D. K.;Baimuratov, O. A.;Karimzhan, N.;Chinibayev, Y.', 'Title': 'Analysis and development of agent architecture for pest control systems', 'Type': 'Conference Paper', 'Link': None, 'Year': '2015', 'Where published': 'Procedia Computer Science', 'PP.': '139-144', 'Volume': '56', 'KeyWords': 'Agent | Agent architecture | Coltrol | Multi-agent systems | Pest control systems'},
           {'Site': 'Scopus', 'Authors': 'Uskenbayeva, R. K.;Kuandykov, A. A.;Cho, Y. I.;Kozhamzharova, D. K.;Baimuratov, O. A.', 'Title': 'Main principles of task distribution in multi-agent systems and defining basic parameters', 'Type': 'Conference Paper', 'Link': None, 'Year': '16 December 2014', 'Where published': 'International Conference on Control, Automation and Systems', 'PP.': '1471-1474', 'Volume': None, 'KeyWords': 'agents | distribution of tasks | multi-agent system'},
           {'Site': 'Scopus', 'Authors': 'Kuandykov, Abu A.;Baimuratov, Olimzhon A.;Kozhamzharova, Dinara K.;Karimzhan, Nurlan B.', 'Title': 'Design and construction a model of remote control software mobile robot for MAS', 'Type': 'Conference Paper', 'Link': None, 'Year': '2014', 'Where published': '8th IEEE International Conference on Application of Information and Communication Technologies, AICT 2014 - Conference Proceedings', 'PP.': None, 'Volume': None, 'KeyWords': 'Mobile robot | Multi-agent system | Remote control | Robotic agents | Teleoperation'},
           {'Site': 'Scopus', 'Authors': 'Tokenov, Nurmakhan;Dzhamanbayev, Muratkali;Bekbayev, Amangeldi;Eskendirova, Damelya;Baimuratov, Olimzhon', 'Title': 'Mathematical model for calculating aerodynamic characteristics of overhead transmission lines', 'Type': 'Conference Paper', 'Link': None, 'Year': '2014', 'Where published': 'Applied Mechanics and Materials', 'PP.': '52-59', 'Volume': '610', 'KeyWords': 'Aerodynamic characteristics | Fluctuations | Galloping | Overhed transmission lines'},
           {'Site': 'Scopus', 'Authors': 'Yessenturayeva, Laura Bigelovna;Mendakulov, Zhassulan Korobaevich;Kozhamzharova, Dinara Khanatovna;Baimuratov, Olimzhon Abdukhakimovich', 'Title': 'Using of MIMO-OFDM technology in radio access systems', 'Type': 'Article', 'Link': None, 'Year': '2014', 'Where published': 'World Applied Sciences Journal', 'PP.': '133-137', 'Volume': '31', 'KeyWords': 'Channel coding | LTE | MIMO | OFDM | Symmetric channel'},
           {'Site': 'Scopus', 'Authors': 'Aitchanov, Bekmurza H.;Nikulin, Vladimir V.;Baimuratov, Olimzhon A.', 'Title': 'Mathematical modeling of digital pulse-frequency modulation control systems developed for objects with transport delay', 'Type': 'Conference Paper', 'Link': None, 'Year': '2013', 'Where published': '2013 25th Chinese Control and Decision Conference, CCDC 2013', 'PP.': '1407-1411', 'Volume': None, 'KeyWords': 'Control System | Dynamic Reset | Pulse Forming | Pulse-Frequency Modulation | Volterra Model'}]

def getbibtext(pub_list):
    ResText = ''
    for item in pub_list:
        ResText = ResText +'\item' +  str(item['Authors']) + ', ' \
                  + '\href{' + str(item['Link']) + '}{' + str(item['Title']) + '}, '\
                  + str(item['Where published']) + ', ' \
                  + str(item['Year'])
        if str(item['PP.'])!= 'None':
            ResText = ResText +  ', pp.' + str(item['PP.']) + '.'
    return ResText
def run():
    ResText = getbibtext(PubList)
    #open tex template
    with open('../april/templates/april/sometexfile.tex') as template_file:
        global latex_code
        latex_code = template_file.read()
        print(latex_code)
    # write and save tex file
    tex_filename = 'publications.tex'
    with open(tex_filename, 'w') as latex_file:
        latex_code = latex_code.replace(r'\VAR{NAME}', AuthorInf['Name'])
        latex_code = latex_code.replace(r'\VAR{EMAIL}', AuthorInf['Email'])
        latex_code = latex_code.replace(r'\VAR{POS}', AuthorInf['Position'])
        latex_code = latex_code.replace(r'\VAR{AFF}', AuthorInf['Affilation'])
        latex_code = latex_code.replace(r'\VAR{PUBLIST}', ResText)
        latex_file.write(latex_code)
    print(latex_code)
    print(f'Generated {tex_filename}')

    os.system("pdflatex publications.tex")


run()