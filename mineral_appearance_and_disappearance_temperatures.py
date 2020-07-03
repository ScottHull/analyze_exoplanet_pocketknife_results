from mineraology import Mineralogy

m = Mineralogy()

all_appearance_and_disappearance_temperatures = m.get_appearance_and_disappearance_temperatures()
all_minerals_found = m.get_all_unique_minerals_found()

print(all_minerals_found)
print(all_appearance_and_disappearance_temperatures['kepler_bsp']['2M18495813+4358487'])