from DataRetriever import DataRetriever

open_data = DataRetriever()

#load all the files
year1hour = open_data.get_data("All-Subsystems-hour-Year1.pkl")
year2hour = open_data.get_data("All-Subsystems-hour-Year2.pkl")

# year1min = open_data.get_data("All-Subsystems-minute-Year1.pkl")
year2min = open_data.get_data("All-Subsystems-minute-Year2.pkl")

year2hour = year2min[['Timestamp', 'PV_PVSystem1ACEnergyOSEACPV1OS', 'Elec_PowerPV1of2', 'PV_PowerFactor3PhTotalPF3PhT1', 'PV_PVSystem1ACPowerOSPACPV1OS', 'PV_Watts3PhTotalW3PhT1']]