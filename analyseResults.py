def analyseText(string):
    tests = string.split("Test")
    testAverages = []
    for test in tests:
        lines = test.split("\n")
        gameLineNums = []
        resultsLineNums = []
        bounds = {}
        for lineNum in range(len(lines)):
            if lines[lineNum]:
                if lines[lineNum][0] == "G":
                    gameLineNums.append(lineNum)
                elif lines[lineNum][0] == "(":
                    resultsLineNums.append(lineNum)

        for index in range(len(gameLineNums)):
            bounds[gameLineNums[index]] = resultsLineNums[index]

        gameplayLines = []
        for start, end in bounds.items():
            # gameplayLines.append(lines[start+1:end])
            gameplayLinesList = lines[start+1:end]
            for index in range(len(gameplayLinesList)):
                gameplayLinesList[index] = gameplayLinesList[index].replace("Time to execute 3000 iterations: ", "")
            gameplayLines.append(gameplayLinesList)
        # print(gameplayLines)

        totals = {}
        for gameNum in range(len(gameplayLines)):
            for i in range(len(gameplayLines[gameNum])):
                num = float(gameplayLines[gameNum][i].replace("s", ""))
                if i not in list(totals.keys()):
                    totals[i] = [num, 1]
                else:
                    totals[i][0] += num
                    totals[i][1] += 1

        for moveNum, totalsList in totals.items():
            totals[moveNum] = totalsList[0]/totalsList[1]

        testAverages.append(totals)

    for i in range(len(testAverages)):
        print(f"\n\n\nTest {i} Average time to execute 3000 iterations\n{testAverages}")

analyseText('''
Test 3a
{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsCS::', 'B1': 'minimax3'}
Game 1
Time to execute 3000 iterations: 104.62818884849548s
Time to execute 3000 iterations: 93.50250434875488s
Time to execute 3000 iterations: 77.49268770217896s
Time to execute 3000 iterations: 81.30651617050171s
Time to execute 3000 iterations: 65.47161984443665s
Time to execute 3000 iterations: 64.07770705223083s
Time to execute 3000 iterations: 39.46545195579529s
Time to execute 3000 iterations: 23.49124789237976s
('RED', 15)
Game 2
Time to execute 3000 iterations: 110.24280524253845s
Time to execute 3000 iterations: 88.50264692306519s
Time to execute 3000 iterations: 87.9062979221344s
Time to execute 3000 iterations: 68.71830892562866s
Time to execute 3000 iterations: 51.22011685371399s
('RED', 9)
Game 3
Time to execute 3000 iterations: 108.1355550289154s
Time to execute 3000 iterations: 91.05463910102844s
Time to execute 3000 iterations: 76.90343189239502s
Time to execute 3000 iterations: 78.8280520439148s
Time to execute 3000 iterations: 64.22459602355957s
Time to execute 3000 iterations: 57.05272817611694s
Time to execute 3000 iterations: 58.899662017822266s
Time to execute 3000 iterations: 36.418952226638794s
Time to execute 3000 iterations: 29.133841037750244s
Time to execute 3000 iterations: 26.511327981948853s
Time to execute 3000 iterations: 16.780813932418823s
('BLUE', 22)
Game 4
Time to execute 3000 iterations: 101.732430934906s
Time to execute 3000 iterations: 95.88817596435547s
Time to execute 3000 iterations: 79.70436096191406s
Time to execute 3000 iterations: 67.9287040233612s
Time to execute 3000 iterations: 60.5646698474884s
Time to execute 3000 iterations: 49.55061197280884s
Time to execute 3000 iterations: 47.25597405433655s
Time to execute 3000 iterations: 50.07019305229187s
Time to execute 3000 iterations: 42.347468852996826s
Time to execute 3000 iterations: 37.47504997253418s
Time to execute 3000 iterations: 38.01822304725647s
Time to execute 3000 iterations: 24.440194129943848s
Time to execute 3000 iterations: 15.761017322540283s
Time to execute 3000 iterations: 10.853286743164062s
Time to execute 3000 iterations: 5.77092981338501s
Time to execute 3000 iterations: 2.4086241722106934s
Time to execute 3000 iterations: 1.9073486328125e-06s
Time to execute 3000 iterations: 9.5367431640625e-07s
Time to execute 3000 iterations: 9.5367431640625e-07s
('RED', 37)
Game 5
Time to execute 3000 iterations: 111.4062430858612s
Time to execute 3000 iterations: 87.7674810886383s
Time to execute 3000 iterations: 80.78754711151123s
Time to execute 3000 iterations: 70.52913618087769s
Time to execute 3000 iterations: 42.12323307991028s
Time to execute 3000 iterations: 37.829761028289795s
Time to execute 3000 iterations: 19.777211904525757s
('RED', 13)
{'DRAW': [0, 0], 'RED': [4, 18.5], 'BLUE': [1, 22.0]}


{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsCS::', 'B1': 'minimax3'}
Game 1
Time to execute 3000 iterations: 101.13498115539551s
Time to execute 3000 iterations: 83.20522403717041s
Time to execute 3000 iterations: 65.27942490577698s
Time to execute 3000 iterations: 76.70161414146423s
Time to execute 3000 iterations: 53.447624921798706s
Time to execute 3000 iterations: 53.76198601722717s
Time to execute 3000 iterations: 31.911540031433105s
Time to execute 3000 iterations: 36.156779050827026s
Time to execute 3000 iterations: 28.24085783958435s
Time to execute 3000 iterations: 26.935760259628296s
Time to execute 3000 iterations: 22.809677124023438s
Time to execute 3000 iterations: 15.632696151733398s
('BLUE', 25)
Game 2
Time to execute 3000 iterations: 105.53876423835754s
Time to execute 3000 iterations: 77.45572996139526s
Time to execute 3000 iterations: 67.79583692550659s
Time to execute 3000 iterations: 71.80548620223999s
Time to execute 3000 iterations: 59.41480493545532s
Time to execute 3000 iterations: 57.46768832206726s
Time to execute 3000 iterations: 48.46332597732544s
Time to execute 3000 iterations: 41.48754286766052s
Time to execute 3000 iterations: 40.14151191711426s
Time to execute 3000 iterations: 28.520084857940674s
Time to execute 3000 iterations: 23.022720098495483s
('RED', 22)
Game 3
Time to execute 3000 iterations: 100.46364116668701s
Time to execute 3000 iterations: 74.5436520576477s
Time to execute 3000 iterations: 79.31848883628845s
Time to execute 3000 iterations: 75.81619715690613s
Time to execute 3000 iterations: 74.99788403511047s
Time to execute 3000 iterations: 61.21339702606201s
Time to execute 3000 iterations: 45.66022491455078s
('BLUE', 15)
Game 4
Time to execute 3000 iterations: 108.50826811790466s
Time to execute 3000 iterations: 102.29314398765564s
Time to execute 3000 iterations: 94.32721304893494s
Time to execute 3000 iterations: 78.93676209449768s
Time to execute 3000 iterations: 60.58037185668945s
Time to execute 3000 iterations: 52.04953908920288s
Time to execute 3000 iterations: 38.067370891571045s
Time to execute 3000 iterations: 38.764662981033325s
Time to execute 3000 iterations: 32.25533699989319s
Time to execute 3000 iterations: 24.011237144470215s
Time to execute 3000 iterations: 21.950170040130615s
Time to execute 3000 iterations: 14.922493934631348s
Time to execute 3000 iterations: 13.51807689666748s
('BLUE', 27)
Game 5
Time to execute 3000 iterations: 119.75825095176697s
Time to execute 3000 iterations: 99.13829016685486s
Time to execute 3000 iterations: 93.58960580825806s
Time to execute 3000 iterations: 81.32792711257935s
Time to execute 3000 iterations: 70.7227110862732s
Time to execute 3000 iterations: 48.242571115493774s
Time to execute 3000 iterations: 53.52526116371155s
Time to execute 3000 iterations: 48.33051109313965s
Time to execute 3000 iterations: 46.86240315437317s
Time to execute 3000 iterations: 35.50174593925476s
Time to execute 3000 iterations: 20.224975109100342s
('BLUE', 23)
{'DRAW': [0, 0], 'BLUE': [4, 22.5], 'RED': [1, 22.0]}


Test 3b
{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsDS::', 'B1': 'minimax3'}
Game 1
Time to execute 3000 iterations: 21.85984992980957s
Time to execute 3000 iterations: 20.08633303642273s
Time to execute 3000 iterations: 16.901827096939087s
Time to execute 3000 iterations: 18.89634609222412s
Time to execute 3000 iterations: 19.91841411590576s
Time to execute 3000 iterations: 14.9598388671875s
Time to execute 3000 iterations: 15.371027946472168s
Time to execute 3000 iterations: 11.122841119766235s
Time to execute 3000 iterations: 10.588754892349243s
Time to execute 3000 iterations: 10.684388637542725s
Time to execute 3000 iterations: 11.080641031265259s
Time to execute 3000 iterations: 9.03712010383606s
Time to execute 3000 iterations: 7.566370010375977s
Time to execute 3000 iterations: 4.0592100620269775s
Time to execute 3000 iterations: 3.3727710247039795s
Time to execute 3000 iterations: 2.958428144454956s
('BLUE', 32)
Game 2
Time to execute 3000 iterations: 22.395240306854248s
Time to execute 3000 iterations: 19.465476751327515s
Time to execute 3000 iterations: 17.91014289855957s
Time to execute 3000 iterations: 15.789346933364868s
Time to execute 3000 iterations: 15.320913791656494s
Time to execute 3000 iterations: 14.021485090255737s
Time to execute 3000 iterations: 9.393547058105469s
Time to execute 3000 iterations: 8.79249095916748s
Time to execute 3000 iterations: 3.4689269065856934s
('RED', 17)
Game 3
Time to execute 3000 iterations: 21.516884088516235s
Time to execute 3000 iterations: 19.356003761291504s
Time to execute 3000 iterations: 17.797078847885132s
Time to execute 3000 iterations: 18.46483302116394s
Time to execute 3000 iterations: 18.95988917350769s
Time to execute 3000 iterations: 15.320000886917114s
Time to execute 3000 iterations: 15.146586179733276s
Time to execute 3000 iterations: 11.628205060958862s
Time to execute 3000 iterations: 11.436025142669678s
Time to execute 3000 iterations: 10.863877296447754s
Time to execute 3000 iterations: 12.42173981666565s
Time to execute 3000 iterations: 10.234217882156372s
Time to execute 3000 iterations: 7.028407096862793s
Time to execute 3000 iterations: 5.308715105056763s
('BLUE', 28)
Game 4
Time to execute 3000 iterations: 26.18610692024231s
Time to execute 3000 iterations: 21.721837997436523s
Time to execute 3000 iterations: 20.768484830856323s
Time to execute 3000 iterations: 18.365705966949463s
Time to execute 3000 iterations: 17.08932900428772s
Time to execute 3000 iterations: 11.155855178833008s
Time to execute 3000 iterations: 5.504882097244263s
('RED', 13)
Game 5
Time to execute 3000 iterations: 24.882251977920532s
Time to execute 3000 iterations: 26.064228057861328s
Time to execute 3000 iterations: 21.646818161010742s
Time to execute 3000 iterations: 16.929824829101562s
Time to execute 3000 iterations: 27.261538982391357s
Time to execute 3000 iterations: 12.315453052520752s
Time to execute 3000 iterations: 6.004103899002075s
('RED', 13)
{'DRAW': [0, 0], 'RED': [3, 14.333333333333334], 'BLUE': [2, 30.0]}


{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsDS::', 'B1': 'minimax3'}
Game 1
Time to execute 3000 iterations: 22.70685911178589s
Time to execute 3000 iterations: 21.652517795562744s
Time to execute 3000 iterations: 14.50298285484314s
Time to execute 3000 iterations: 15.584956169128418s
Time to execute 3000 iterations: 19.8213529586792s
Time to execute 3000 iterations: 17.371580123901367s
Time to execute 3000 iterations: 14.839402914047241s
Time to execute 3000 iterations: 15.155237913131714s
Time to execute 3000 iterations: 12.360783815383911s
Time to execute 3000 iterations: 10.395313739776611s
Time to execute 3000 iterations: 8.77611231803894s
Time to execute 3000 iterations: 6.868677854537964s
Time to execute 3000 iterations: 8.699265718460083s
Time to execute 3000 iterations: 5.868772983551025s
('BLUE', 29)
Game 2
Time to execute 3000 iterations: 22.310240983963013s
Time to execute 3000 iterations: 19.85295009613037s
Time to execute 3000 iterations: 20.2364239692688s
Time to execute 3000 iterations: 17.905611038208008s
Time to execute 3000 iterations: 17.741760969161987s
Time to execute 3000 iterations: 14.315744876861572s
Time to execute 3000 iterations: 9.292344808578491s
Time to execute 3000 iterations: 6.932821035385132s
('RED', 16)
Game 3
Time to execute 3000 iterations: 21.1541748046875s
Time to execute 3000 iterations: 17.23084807395935s
Time to execute 3000 iterations: 17.59982919692993s
Time to execute 3000 iterations: 14.843823909759521s
Time to execute 3000 iterations: 15.745544910430908s
Time to execute 3000 iterations: 13.079344987869263s
Time to execute 3000 iterations: 4.590872049331665s
('RED', 14)
Game 4
Time to execute 3000 iterations: 23.164130687713623s
Time to execute 3000 iterations: 20.20872402191162s
Time to execute 3000 iterations: 20.317404985427856s
Time to execute 3000 iterations: 18.67507576942444s
Time to execute 3000 iterations: 19.697849988937378s
Time to execute 3000 iterations: 15.888346195220947s
Time to execute 3000 iterations: 10.077987909317017s
Time to execute 3000 iterations: 5.446126937866211s
('RED', 16)
Game 5
Time to execute 3000 iterations: 21.643251180648804s
Time to execute 3000 iterations: 18.18253803253174s
Time to execute 3000 iterations: 14.41313886642456s
Time to execute 3000 iterations: 17.23831796646118s
Time to execute 3000 iterations: 13.701341152191162s
Time to execute 3000 iterations: 15.96217679977417s
Time to execute 3000 iterations: 14.869505882263184s
Time to execute 3000 iterations: 14.328367948532104s
Time to execute 3000 iterations: 13.649129152297974s
Time to execute 3000 iterations: 11.549087047576904s
Time to execute 3000 iterations: 9.698129892349243s
Time to execute 3000 iterations: 6.018992900848389s
('RED', 24)
{'DRAW': [0, 0], 'BLUE': [1, 29.0], 'RED': [4, 17.5]}


Test 3c
{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsCS::', 'B1': 'mctsDS::'}
Game 1
Time to execute 3000 iterations: 114.76869010925293s
Time to execute 3000 iterations: 22.446253061294556s
Time to execute 3000 iterations: 103.9914779663086s
Time to execute 3000 iterations: 19.8278169631958s
Time to execute 3000 iterations: 94.30744981765747s
Time to execute 3000 iterations: 18.42594313621521s
Time to execute 3000 iterations: 74.9913079738617s
Time to execute 3000 iterations: 13.618665933609009s
Time to execute 3000 iterations: 58.887588024139404s
Time to execute 3000 iterations: 15.432760000228882s
Time to execute 3000 iterations: 48.78752279281616s
Time to execute 3000 iterations: 11.151440858840942s
Time to execute 3000 iterations: 32.43370699882507s
Time to execute 3000 iterations: 12.16063904762268s
Time to execute 3000 iterations: 37.715171098709106s
Time to execute 3000 iterations: 9.60204005241394s
Time to execute 3000 iterations: 25.311479806900024s
Time to execute 3000 iterations: 9.986861944198608s
Time to execute 3000 iterations: 17.73720407485962s
Time to execute 3000 iterations: 7.997274160385132s
Time to execute 3000 iterations: 12.500380039215088s
Time to execute 3000 iterations: 5.643022060394287s
Time to execute 3000 iterations: 7.260583877563477s
Time to execute 3000 iterations: 4.453529119491577s
Time to execute 3000 iterations: 5.540016174316406s
Time to execute 3000 iterations: 3.8354663848876953s
Time to execute 3000 iterations: 2.8573238849639893s
Time to execute 3000 iterations: 3.647885799407959s
Time to execute 3000 iterations: 2.1457672119140625e-06s
Time to execute 3000 iterations: 2.668044090270996s
Time to execute 3000 iterations: 1.1920928955078125e-06s
Time to execute 3000 iterations: 2.400280237197876s
Time to execute 3000 iterations: 2.1457672119140625e-06s
Time to execute 3000 iterations: 2.110522985458374s
('BLUE', 34)
Game 2
Time to execute 3000 iterations: 123.5726420879364s
Time to execute 3000 iterations: 21.27488398551941s
Time to execute 3000 iterations: 88.89249610900879s
Time to execute 3000 iterations: 16.9100501537323s
Time to execute 3000 iterations: 83.54356694221497s
Time to execute 3000 iterations: 17.647663116455078s
Time to execute 3000 iterations: 81.46670007705688s
Time to execute 3000 iterations: 16.217188119888306s
Time to execute 3000 iterations: 66.15288186073303s
Time to execute 3000 iterations: 14.647197008132935s
Time to execute 3000 iterations: 60.87564730644226s
Time to execute 3000 iterations: 17.36112403869629s
Time to execute 3000 iterations: 63.63437604904175s
Time to execute 3000 iterations: 16.234562873840332s
Time to execute 3000 iterations: 54.71710991859436s
Time to execute 3000 iterations: 13.615355014801025s
Time to execute 3000 iterations: 34.38901209831238s
Time to execute 3000 iterations: 8.74133586883545s
Time to execute 3000 iterations: 32.29382085800171s
('RED', 19)
Game 3
Time to execute 3000 iterations: 101.61743187904358s
Time to execute 3000 iterations: 19.75886297225952s
Time to execute 3000 iterations: 89.88270092010498s
Time to execute 3000 iterations: 16.632221937179565s
Time to execute 3000 iterations: 81.78761005401611s
Time to execute 3000 iterations: 16.879649877548218s
Time to execute 3000 iterations: 78.72556209564209s
Time to execute 3000 iterations: 17.378061056137085s
Time to execute 3000 iterations: 75.1817536354065s
Time to execute 3000 iterations: 17.916001081466675s
Time to execute 3000 iterations: 74.17266321182251s
Time to execute 3000 iterations: 16.643275022506714s
Time to execute 3000 iterations: 59.095341205596924s
Time to execute 3000 iterations: 15.55744481086731s
Time to execute 3000 iterations: 48.73814916610718s
Time to execute 3000 iterations: 13.783159971237183s
Time to execute 3000 iterations: 44.047900915145874s
Time to execute 3000 iterations: 11.819879055023193s
Time to execute 3000 iterations: 30.650864839553833s
Time to execute 3000 iterations: 11.58425498008728s
Time to execute 3000 iterations: 29.854870080947876s
Time to execute 3000 iterations: 11.136513948440552s
Time to execute 3000 iterations: 23.407254934310913s
Time to execute 3000 iterations: 9.621932983398438s
Time to execute 3000 iterations: 15.924888849258423s
Time to execute 3000 iterations: 7.776868104934692s
Time to execute 3000 iterations: 17.155842065811157s
('RED', 27)
Game 4
Time to execute 3000 iterations: 100.16899299621582s
Time to execute 3000 iterations: 19.319074630737305s
Time to execute 3000 iterations: 77.23074221611023s
Time to execute 3000 iterations: 27.68116807937622s
Time to execute 3000 iterations: 72.19740509986877s
Time to execute 3000 iterations: 14.147254943847656s
Time to execute 3000 iterations: 75.22212505340576s
Time to execute 3000 iterations: 15.586102962493896s
Time to execute 3000 iterations: 71.17997312545776s
Time to execute 3000 iterations: 14.722791910171509s
Time to execute 3000 iterations: 56.33296179771423s
Time to execute 3000 iterations: 13.65129804611206s
Time to execute 3000 iterations: 46.82068204879761s
Time to execute 3000 iterations: 11.888934850692749s
Time to execute 3000 iterations: 35.96900415420532s
Time to execute 3000 iterations: 9.248749256134033s
Time to execute 3000 iterations: 29.3589608669281s
Time to execute 3000 iterations: 8.325893878936768s
Time to execute 3000 iterations: 15.59737491607666s
('RED', 19)
Game 5
Time to execute 3000 iterations: 99.46494603157043s
Time to execute 3000 iterations: 17.518690824508667s
Time to execute 3000 iterations: 93.03358912467957s
Time to execute 3000 iterations: 17.487175226211548s
Time to execute 3000 iterations: 80.28562092781067s
Time to execute 3000 iterations: 16.722754955291748s
Time to execute 3000 iterations: 70.62843585014343s
Time to execute 3000 iterations: 15.330718994140625s
Time to execute 3000 iterations: 60.21566104888916s
Time to execute 3000 iterations: 17.874183177947998s
Time to execute 3000 iterations: 59.04243803024292s
Time to execute 3000 iterations: 14.597289800643921s
Time to execute 3000 iterations: 54.737565755844116s
Time to execute 3000 iterations: 14.848055124282837s
Time to execute 3000 iterations: 51.52805495262146s
Time to execute 3000 iterations: 13.274038076400757s
Time to execute 3000 iterations: 36.27262020111084s
Time to execute 3000 iterations: 12.135293960571289s
Time to execute 3000 iterations: 38.311363220214844s
Time to execute 3000 iterations: 7.756837844848633s
Time to execute 3000 iterations: 18.46656894683838s
('RED', 21)
{'DRAW': [0, 0], 'RED': [4, 21.5], 'BLUE': [1, 34.0]}


{'R1': 'RED', 'B1': 'BLUE'}
{'R1': 'mctsCS::', 'B1': 'mctsDS::'}
Game 1
Time to execute 3000 iterations: 19.06289315223694s
Time to execute 3000 iterations: 85.40609002113342s
Time to execute 3000 iterations: 16.593454122543335s
Time to execute 3000 iterations: 86.5298490524292s
Time to execute 3000 iterations: 16.85237979888916s
Time to execute 3000 iterations: 70.3463568687439s
Time to execute 3000 iterations: 15.00581979751587s
Time to execute 3000 iterations: 58.89390587806702s
Time to execute 3000 iterations: 12.463154077529907s
Time to execute 3000 iterations: 50.422311782836914s
Time to execute 3000 iterations: 14.571276664733887s
Time to execute 3000 iterations: 55.48880696296692s
Time to execute 3000 iterations: 13.368644952774048s
Time to execute 3000 iterations: 49.410585165023804s
Time to execute 3000 iterations: 10.776281833648682s
Time to execute 3000 iterations: 34.500568151474s
('RED', 16)
Game 2
Time to execute 3000 iterations: 18.878594160079956s
Time to execute 3000 iterations: 91.49818539619446s
Time to execute 3000 iterations: 17.394701957702637s
Time to execute 3000 iterations: 76.92462921142578s
Time to execute 3000 iterations: 16.48914408683777s
Time to execute 3000 iterations: 68.42925715446472s
Time to execute 3000 iterations: 13.600054025650024s
Time to execute 3000 iterations: 55.56826591491699s
Time to execute 3000 iterations: 13.590629816055298s
Time to execute 3000 iterations: 49.18586611747742s
Time to execute 3000 iterations: 11.202473163604736s
Time to execute 3000 iterations: 41.647756814956665s
Time to execute 3000 iterations: 8.306570053100586s
Time to execute 3000 iterations: 30.959811210632324s
Time to execute 3000 iterations: 8.353973150253296s
Time to execute 3000 iterations: 26.377298831939697s
Time to execute 3000 iterations: 8.325716018676758s
Time to execute 3000 iterations: 25.625128269195557s
Time to execute 3000 iterations: 7.302600860595703s
Time to execute 3000 iterations: 16.73091697692871s
Time to execute 3000 iterations: 4.0922088623046875s
Time to execute 3000 iterations: 9.068694829940796s
('RED', 22)
Game 3
Time to execute 3000 iterations: 18.84366512298584s
Time to execute 3000 iterations: 93.35242199897766s
Time to execute 3000 iterations: 17.43581223487854s
Time to execute 3000 iterations: 82.23323702812195s
Time to execute 3000 iterations: 16.62973165512085s
Time to execute 3000 iterations: 74.2008740901947s
Time to execute 3000 iterations: 13.215143918991089s
Time to execute 3000 iterations: 54.78508377075195s
Time to execute 3000 iterations: 4.919992923736572s
('BLUE', 9)
Game 4
Time to execute 3000 iterations: 19.071160078048706s
Time to execute 3000 iterations: 89.69561386108398s
Time to execute 3000 iterations: 17.420330047607422s
Time to execute 3000 iterations: 76.03524112701416s
Time to execute 3000 iterations: 16.304183959960938s
Time to execute 3000 iterations: 68.58873081207275s
Time to execute 3000 iterations: 13.349864959716797s
Time to execute 3000 iterations: 52.39861607551575s
Time to execute 3000 iterations: 10.507017850875854s
Time to execute 3000 iterations: 44.52918481826782s
Time to execute 3000 iterations: 11.287930965423584s
Time to execute 3000 iterations: 38.77752995491028s
Time to execute 3000 iterations: 9.425532817840576s
Time to execute 3000 iterations: 35.26244783401489s
Time to execute 3000 iterations: 14.568595886230469s
Time to execute 3000 iterations: 25.623339891433716s
Time to execute 3000 iterations: 7.312566041946411s
Time to execute 3000 iterations: 20.552670001983643s
Time to execute 3000 iterations: 6.0749688148498535s
Time to execute 3000 iterations: 15.195275783538818s
Time to execute 3000 iterations: 3.46636700630188s
('BLUE', 21)
Game 5
Time to execute 3000 iterations: 18.82184886932373s
Time to execute 3000 iterations: 92.20615720748901s
Time to execute 3000 iterations: 17.065008878707886s
Time to execute 3000 iterations: 74.25147986412048s
Time to execute 3000 iterations: 15.58327317237854s
Time to execute 3000 iterations: 67.44663882255554s
Time to execute 3000 iterations: 15.346489191055298s
Time to execute 3000 iterations: 65.03967475891113s
Time to execute 3000 iterations: 14.449995756149292s
Time to execute 3000 iterations: 59.92913889884949s
Time to execute 3000 iterations: 11.737052917480469s
Time to execute 3000 iterations: 40.75131893157959s
Time to execute 3000 iterations: 9.82186484336853s
Time to execute 3000 iterations: 38.83463907241821s
Time to execute 3000 iterations: 11.499553918838501s
Time to execute 3000 iterations: 34.96526384353638s
Time to execute 3000 iterations: 6.795438051223755s
Time to execute 3000 iterations: 24.103535652160645s
('RED', 18)
{'DRAW': [0, 0], 'BLUE': [2, 15.0], 'RED': [3, 18.666666666666668]}
''')
