__license__ = 'GNU Public License Version 3, https://www.gnu.org/licenses/gpl-3.0.en.html'
__copyright__ = "Copyright (C) 2020, Dev@BernCodes.com - Released under terms of the GPLv3 License"

from bitstring import BitArray, BitStream
import logging

Valid_Dominos = [95, 111, 119, 123, 125, 126, 159, 175, 183, 187, 189, 190, 207, 215, 219, 221, 222, 231, 235, 237, 238, 243, 245, 246, 249, 250, 252, 287, 303, 
311, 315, 317, 318, 335, 343, 347, 349, 350, 359, 363, 365, 366, 371, 373, 374, 377, 378, 380, 399, 407, 411, 413, 414, 423, 427, 429, 430, 435, 
437, 438, 441, 442, 444, 455, 459, 461, 462, 467, 469, 470, 473, 474, 476, 483, 485, 486, 489, 490, 492, 497, 498, 500, 543, 559, 567, 571, 573, 
574, 591, 599, 603, 605, 606, 615, 619, 621, 622, 627, 629, 630, 633, 634, 636, 655, 663, 667, 669, 670, 679, 683, 685, 686, 691, 693, 694, 697, 
698, 700, 711, 715, 717, 718, 723, 725, 726, 729, 730, 732, 739, 741, 742, 745, 746, 748, 753, 754, 783, 791, 795, 797, 798, 807, 811, 813, 814, 
819, 821, 822, 825, 826, 828, 839, 843, 845, 846, 851, 853, 854, 857, 858, 860, 867, 869, 870, 873, 874, 881, 882, 903, 907, 909, 910, 915, 917, 
918, 921, 922, 931, 933, 934, 937, 938, 945, 946, 963, 965, 966, 969, 970, 977, 978, 993, 994, 1055, 1071, 1079, 1083, 1085, 1086, 1103, 1111, 1115, 1117, 1118, 1127, 1131, 1133, 1134, 1139, 1141, 1142, 1145, 1146, 1167, 1175, 1179, 1181, 1182, 1191, 1195, 1197, 1198, 1203, 1205, 1206, 1209, 1210, 1223, 1227, 1229, 1230, 1235, 1237, 1238, 1241, 1242, 1251, 1253, 1254, 1257, 1258, 1265, 1295, 1303, 1307, 1309, 1310, 1319, 1323, 1325, 1326, 1331, 1333, 1334, 1337, 1338, 1351, 1355, 1357, 1358, 1363, 1365, 1366, 1369, 1370, 1379, 1381, 1382, 1385, 1393, 1415, 1419, 1421, 1422, 1427, 1429, 1430, 1433, 1443, 1445, 1446, 1449, 1457, 1475, 1477, 1478, 1481, 1489, 1505, 1551, 1559, 1563, 1565, 1566, 1575, 1579, 1581, 1582, 
1587, 1589, 1590, 1593, 1607, 1611, 1613, 1614, 1619, 1621, 1622, 1625, 1635, 1637, 1641, 1649, 1671, 1675, 1677, 1678, 1683, 1685, 1689, 1699, 1701, 1705, 1713, 1731, 1733, 1737, 1745, 1761, 1799, 1803, 1805, 1811, 1813, 1817, 1827, 1829, 1833, 1841, 1859, 1861, 1865, 1873, 1889, 1923, 1925, 1929, 1937, 1953, 1985, 2079, 2095, 2103, 2107, 2109, 2127, 2135, 2139, 2141, 2151, 2155, 2157, 2163, 2165, 2169, 2191, 2199, 2203, 2205, 2215, 2219, 2221, 2227, 2229, 2233, 2247, 2251, 2253, 2259, 2261, 2265, 2275, 2277, 2281, 2319, 2327, 2331, 2333, 2343, 2347, 2349, 2355, 2357, 2361, 2375, 2379, 2381, 2387, 2389, 2393, 2403, 2405, 2439, 2443, 2445, 2451, 2453, 2467, 2469, 2499, 2501, 2575, 2583, 2587, 2589, 2599, 2603, 2605, 2611, 2613, 2631, 2635, 2637, 2643, 2645, 2659, 2695, 2699, 2701, 2707, 2723, 2755, 2823, 2827, 2835, 2851, 2883, 2947, 3087, 3095, 3099, 3111, 
3115, 3123, 3143, 3147, 3155, 3207, 3211, 3335]


def GenerateValidDominos(Start = 0, End = 4095):
    logging.debug("Checking Domino Values from {} to {}" . format(Start, End))

    bPass = 1
    Row1 = 0
    Row2 = 0
    ValidValues = []

    for x in range(Start,(End+1),1):
        bPass = True
        DPips = BitArray('0x000')
        DPips.uint = x
        Row1 = DPips[:6]
        Row2 = DPips[-6:]
        logging.debug("Index Value:{} Binary Value:{}" .format(x,DPips.bin))
        
        #Row 1 and 2 Pip Count
        R1_PC = len(list(Row1.findall([1])))
        R2_PC = len(list(Row2.findall([1])))

        #Domino must have at least 1 pip, no more than 5, and a total of 6.        
        if (R1_PC > 5) or (R1_PC < 1): bPass = False
        if (R2_PC > 5) or (R2_PC < 1): bPass = False
        if (R1_PC + R2_PC) != 6: bPass = False

        logging.debug("Row 1 Value:{} Binary Value:{} Pip Count:{}" .format(Row1.uint, Row1.bin, R1_PC))
        logging.debug("Row 2 Value:{} Binary Value:{} Pip Count:{}" .format(Row2.uint, Row2.bin, R2_PC))
        logging.debug("Pip count validity: {}" . format(bPass))

        #Generate the reverse of the bit stream.
        DFlip = BitArray('0x000')
        DFlip.uint = x
        DFlip.reverse()
        ReversedValue = DFlip.uint

        logging.debug("Flipped Row Value:{} Binary Value:{}" .format(ReversedValue, DFlip.bin))        

        #The domino is a mirror iamge of itself and is invalid.
        if (ReversedValue == x):
            logging.debug("Mirror Domino")
            bPass = False
        
        #The rotated domino exists as a prior value.
        if (ReversedValue in ValidValues):
            logging.debug("Rotated domino exists previously")
            bPass = False

        #The specified domino passed all rules and is valid.
        if (bPass == True):
            ValidValues.append(x)
            logging.debug("Added Valid Value {}({}) to list." . format(x, DPips.bin))


        logging.debug("---")

    logging.debug(ValidValues)
    return ValidValues

if __name__ == "__main__":
    logging.basicConfig(filename='domino.log',level=logging.DEBUG)
    GeneratedDominos = GenerateValidDominos(0,4095)
    print (GeneratedDominos)
    print ("Found a total of {} dominos" . format(len(GeneratedDominos)))


