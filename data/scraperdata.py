#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from time import sleep
from selenium.common.exceptions import ElementClickInterceptedException


# In[2]:


driver = webdriver.Chrome()
url = 'https://jeux.loro.ch/horses/races'
driver.get(url)

### sélection la course terminé
driver.find_element_by_xpath("""
//*[@id="root"]/main/section/article/div/div/nav[2]/ul/li[2]""").click()
nbCourse = driver.find_element_by_xpath("""
//*[@id="root"]/main/section/article/div/div/nav[2]/ul/li[2]/p[2]""")
print("le nombre de courses terminées: {0}".format(nbCourse.text[:2]))
nombredecourse = int(nbCourse.text[:2])

### sélectionner la section des courses terminées
driver.find_element_by_xpath("""
//*[@id="root"]/main/section/article/div/div/section/ul/li[2]/a/article/section/div[1]""").click()

### le compteur pour la boucle while
counter = 1 
### le temps d'attente entre les clicks 
tempsAttente = 1
## fiche de cheval
listeInfos = [1,2,3,4,8,9,10]
### maintenant on va écrire les données dans un fichier csv 

### nom du fichier csv
name = driver.find_element_by_xpath("""//*[@id="root"]/main/div/article[1]/section[2]/article/h3/span[1]""")
date = driver.find_element_by_xpath("""//*[@id="root"]/main/div/article[1]/div/p/span""")
nameCsv = date.text.replace(' ','_') + name.text.replace(' ','_') 
print("Nom du ficher csv  : " + nameCsv)

### écrire les données dans la un fichier csv
dataFile = 'data_{0}.csv'.format(nameCsv)
with open(dataFile, mode='w') as horseRacing:
    horseRacing.write('NumeroCheval,NomCheval,entraineur,proprietaire,sex,age,race,poid,corde,distanceCourse,cote,nomdeMaman,nomdePapa,courseCourue,victoire,place,gainCarriere,positionArrive\n')
    while counter < nombredecourse : 
        checkCateg  =  driver.find_element_by_xpath("""
        //*[@id="root"]/main/div/article[3]/section/div/div[1]/div[2]/p""")
        if checkCateg.text == 'PLAT':
            print("plat")
            ## cliquer sur arrivé
            driver.find_element_by_xpath("""//*[@id="root"]/main/section/div/div/section/nav/ul/li[2]""").click()

            listePosition = {}
            ### collecter la liste des positions terminées de la course
            position = driver.find_elements_by_class_name("arrivals-tab-content__position-number")

            numberX = driver.find_elements_by_class_name("arrivals-tab-content__separator")
            for p,n in zip(position,numberX):
            #     print(p.text)
                # on ignore les chevaux non-partants
                if p.text != 'NP':
                    if p.text == "N/C":
                        valeur = '0'
                    else:
                        valeur = p.text
                    listePosition[int(n.text)] = valeur
            # print(listePosition)

            ## Trier les clés dans l'ordre
            listePoX ={}
            for k in sorted(listePosition.keys()):
            #     print("%s: %s" % (k, listePosition[k]))
                listePoX[k] = listePosition[k]
            print("---"* 30 )
            print("La position arrivée et le nombre de cheval correspondant: ")
            print(listePoX)

            ## La liste des chevaux partants
            listePartante = []
            [listePartante.append(k) for k in listePoX.keys()]
            print("---"* 30 )
            print("la liste des chevaux partants: ")
            print(listePartante)
            print("---"* 30 )
            ### on va maintenant scraper les données des chevaux
            driver.find_element_by_xpath("""//*[@id="root"]/main/section/div/div/section/nav/ul/li[3]/p""").click()
            ### supprimer des lettres spéciales
            def delSpeLetter(text):
                """
                Remplacer les caractères spéciaux dans les lignes de textes
                """
                for x in text:
                    if x not in 'abcdefghijklmnopqrstuvwyzABCDEFGHIJKLMNOPQRSTUVWYZ ':
                        text = text.replace(x,'')
                return text

            ### on va regarder la liste des cheveaux qui vont faire de la course

            #sleep(tempsAttente)

            ###chercher les informations des chevaux de la course
            links = driver.find_elements_by_class_name('collapsible__section')
            counterLinks = 0
            ### main programe
            for link in links:
                if counterLinks < len(listePartante):
                    ### le numéro de chaque cheval
                    print('--'*20)
                    print(listePartante[counterLinks])
                    number = listePartante[counterLinks]
                    print('--'*20)

                    ### nom des chevaux
                    horseName =driver.find_element_by_xpath("""
                    //*[@id="root"]/main/section/div/div/section/section/div[1]
                    /div/section[{0}]/header/div/div[1]/div/div/div/h2/span[2]
                    """.format(listePartante[counterLinks]))
                    print('Nom du cheval: ' + horseName.text)
                    horse_name = delSpeLetter(horseName.text)

                    ### la côte de chaque cheval
                    odd = driver.find_element_by_xpath("""
                    //*[@id="root"]/main/section/div/div/section/section/div[1]
                    /div/section[{0}]/header/div/div[2]/span
                    """.format(listePartante[counterLinks]))
                    print('la côte: ' + odd.text)
                    cote = odd.text

                    ### cliquer sur les informations de chaque cheval
                    link =driver.find_element_by_xpath("""
                    //*[@id="root"]/main/section/div/div/section/section/div[1]/div/section[{0}]
                    """.format(listePartante[counterLinks]))
                    link.click()
                    sleep(tempsAttente)

                    ### fiche du cheval
                    for x in range(1,11):
                        linke = driver.find_element_by_xpath(
                        """
                        //*[@id="root"]/main/section/div/div/section/section/div[1]
                        /div/section[{0}]/article/section/div/div/div[2]/div/div[2]
                        /div/table/tbody/tr[{1}]/td
                        """.format(listePartante[counterLinks],x))

                        if linke != None:
                            if x == 1 : 
                                print('Entraîneur: ' + linke.text)
                                entraineur = delSpeLetter(linke.text)
                            elif x == 2 :
                                print('Propriétaire: ' + linke.text)
                                proprietaire = delSpeLetter(linke.text)
                            elif x == 3 :
                                print('Sex: ' + linke.text)
                                sex = linke.text
                                if sex == 'MÂLE':
                                    sex = 'MALE'
                            elif x == 4 :
                                print('Âge: ' + linke.text)
                                age = linke.text
                            elif x ==8 : 
                                print('Race: ' + linke.text)
                                race = delSpeLetter(linke.text)
                            elif x == 9 :
                                print('Poids(kg): ' + linke.text.replace('Kg',''))
                                poid = linke.text.replace('Kg','')
                            elif x == 10:
                                print('Corde: ' + linke.text)
                                corde = linke.text

                        else:
                            print('hallo quoi !')
                        #sleep(tempsAttente)

                    ### changer de la fiche 
                    sleep(tempsAttente)
                    changeFiche = driver.find_element_by_xpath("""
                    //*[@id="root"]/main/section/div/div/section/section/div[1]
                    /div/section[{0}]/article/section/div/div/div[3]
                    """.format(listePartante[counterLinks]))
                    changeFiche.click()
                    sleep(tempsAttente)

                    ### Ascendance
                    for z in range (1,3):
                        linkAsc = driver.find_element_by_xpath(
                        """
                        //*[@id="root"]/main/section/div/div/section/section/div[1]
                        /div/section[{0}]/article/section/div/div/div[2]/div/div[3]/
                        div/table[1]/tbody/tr[{1}]/td
                        """.format(listePartante[counterLinks],z))
                        if z == 1 : 
                            print("Nom de la mère: " + linkAsc.text)
                            nomdeMaman = delSpeLetter(linkAsc.text)
                        else:
                            print("Nom du père : "+ linkAsc.text )
                            nomdePapa = delSpeLetter(linkAsc.text)

                    ### performance
                    for y in range(1,5):
                        linkPerf = driver.find_element_by_xpath("""
                        //*[@id="root"]/main/section/div/div/section/section/div[1]
                        /div/section[{0}]/article/section/div/div/div[2]/div/div[3]
                        /div/table[2]/tbody/tr[{1}]/td
                        """.format(listePartante[counterLinks],y))
                        if y == 1:
                            print('Courses courues: ' + linkPerf.text)
                            courseCourue = linkPerf.text
                        elif y ==2: 
                            print('victoires: ' + linkPerf.text)
                            victoire = linkPerf.text
                        elif y == 3 :
                            print( 'Places: ' + linkPerf.text)
                            place = linkPerf.text
                        elif y == 4: 
                            print('Gain en carrière(frs): ' + linkPerf.text.replace("'",""))
                            gainCarriere = linkPerf.text.replace("'","")

                    #sleep(tempsAttente)

                    ### Distance de la course 
                    distance = driver.find_element_by_xpath("""
                    //*[@id="root"]/main/div/article[3]/section/div/div[3]/div[1]/p
                    """)
                    print('Distance(m): ' + distance.text.replace('m',''))
                    distanceCourse = distance.text.replace('m','')

                    ### La position arrivée des chevaux
                    for key in listePoX.keys():
                        if listePartante[counterLinks] == key:
                            positionArrive = listePoX[key]
                            print("La position arrivée : " + positionArrive)


                    counterLinks += 1
                    sleep(tempsAttente)

                else:
                    break

                sleep(tempsAttente)
                horseRacing.write(str(number) + ','+ 
                                  horse_name + ','+ 
                                  entraineur + ','+
                                  proprietaire + ','+ 
                                  sex + ','+
                                  age + ','+
                                  race + ','+
                                  poid + ','+
                                  corde + ','+ 
                                  distanceCourse + ','+
                                  cote + ','+ 
                                  nomdeMaman + ','+ 
                                  nomdePapa + ','+ 
                                  courseCourue + ','+
                                  victoire + ','+
                                  place + ','+
                                  gainCarriere + ','+   
                                  positionArrive + '\n')
                sleep(1)
                target = driver.find_element_by_xpath("""
                //*[@id="root"]/main/div/section/nav/div/ul/li[2]""")
                target.location_once_scrolled_into_view


        else:
            print("Trot attelé")
        ### changer de course
        clickCourse = driver.find_element_by_xpath("""
        //*[@id="root"]/main/div/article[1]/section[2]/div[1]""")
        clickCourse.click()
        counter += 1