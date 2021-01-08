import pandas as pd
import numpy as np
from numpy import savez_compressed
from collections import defaultdict
from numpy import dot
from numpy.linalg import norm
import timeit

from tqdm import tqdm
import pickle
def load_dataset():
    # Define file path
    items_path = "data/items_df.csv"

    # Read file into Dataframe
    items_df = pd.read_csv(items_path)
    return items_df

class Content_Based_KNN():
    def __init__(self, k = 40, sim_options = {}):
        self.k = k
        self.data = load_dataset()
        self.growth_habit = get_growth_habit(self.data)
        self.native_place = get_native_place(self.data)
        self.edible_parts = get_edible_parts(self.data)


    def fit(self, trainset):
        #print(self.growth_habit)
        #print(native_place)
        # compute similarity matrix 2x2 | item x item
        self.similarities = np.zeros((len(trainset.index), len(trainset.index)))

        trainset_length = len(trainset.index)
        #trainset_length = 1000
        #print('species_a, species_b,family_similarity,rank_similarity,genus_similarity,vegetable_similarity, edible_similarity' )
        for index_a in range(trainset_length):
            print(str(index_a),"/",trainset_length)
            start = timeit.default_timer()
            for index_b in range(index_a+1, trainset_length):
                species_a = trainset.iloc[index_a]
                species_b = trainset.iloc[index_b]
                #print(species_a['rank'],species_b['rank'])

                rank_similarity = self.compute_rank_similarity(species_a,species_b)
                genus_similarity = self.compute_genus_similarity(species_a,species_b)
                family_similarity = self.compute_family_similarity(species_a,species_b)
                vegetable_similarity = self.compute_vegetable_similarity(species_a, species_b)
                edible_similarity = self.compute_edible_similarity(species_a, species_b)

                habit_similarity = self.compute_habit_similarity(species_a, species_b)
                native_similarity = self.compute_native_similarity(species_a, species_b)
                #print(species_a,'\t\t', species_b,'\t\t',family_similarity,'\t\t',rank_similarity,'\t\t',genus_similarity,'\t\t',vegetable_similarity,'\t\t', edible_similarity )
                self.similarities[index_a, index_b] =  rank_similarity + genus_similarity + family_similarity + vegetable_similarity + edible_similarity + habit_similarity + native_similarity
                self.similarities[index_b, index_a] = self.similarities[index_a, index_b]
            stop = timeit.default_timer()
            print('Time: ', stop - start)


        savez_compressed('similarity.npz', self.similarities)
        #print(self.similarities)
        return self

        print("...done.")
        return self




    def compute_rank_similarity(self, species_1,species_2):
        #print( species_1['rank'],species_2['rank'])
        if species_1['rank'] == species_2['rank']:
            return 1
        else:
            return 0

    def compute_genus_similarity(self, species_1,species_2):
        #print(species_1['genus_id'], species_2['genus_id'])
        if  species_1['genus_id'] == species_2['genus_id']:
            return 1
        else:
            return 0

    def compute_family_similarity(self, species_1,species_2):
        if species_1['family'] == species_2['family']:
            return 1
        else:
            return 0

    def compute_vegetable_similarity(self, species_1,species_2):
        #print(self.items_df[self.items_df['species_id']==species_1]['vegetable'])
        if species_1['vegetable'] == species_2['vegetable']:
            return 1
        else:
            return 0

    def compute_edible_similarity(self, species_1,species_2):
        if species_1['edible'] == species_2['edible']:
            edible1 = [1]+self.edible_parts[species_1['species_id']]
            edible2 = [1]+self.edible_parts[species_2['species_id']]
            cos_sim = dot(edible1, edible2)/(norm(edible1)*norm(edible2))
            #print(len(edible1))
            #print(trainset.iloc[species_1]['species_id'],":",edible1)
            #print(trainset.iloc[species_2]['species_id'],":",edible2)
            #print("equation eq:",cos_sim)
            return cos_sim
        else:
            return 0

    def compute_habit_similarity(self, species_1,species_2):

        habit1 = self.growth_habit[species_1['species_id']]
        habit2 = self.growth_habit[species_2['species_id']]
        cos_sim = dot(habit1, habit2)/(norm(habit1)*norm(habit2))
        #print(trainset.iloc[species_1]['species_id'],":",habit1)
        #print(trainset.iloc[species_2]['species_id'],":",habit2)
        #print("equation eq:",cos_sim)
        return cos_sim

    def compute_native_similarity(self, species_1,species_2):
        native1 = self.native_place[species_1['species_id']]
        native2 = self.native_place[species_2['species_id']]
        cos_sim = dot(native1, native2)/(norm(native1)*norm(native2))
        #print(len(native1))
        #print(trainset.iloc[species_1]['species_id'],":",native1)
        #print(trainset.iloc[species_2]['species_id'],":",native2)
        #print("equation eq:",cos_sim)
        return cos_sim

    def estimate(id, trainset, similarities):
        #if not (self.trainset.knows_user(u) and self.trainset.knows_item(i)):
            #raise PredictionImpossible('User and/or item is unkown.')
        """
        k-nearest-neighbors:
            a.	Compute the similarity score between all species in the database
            b.	Select k species with the highest similarity to the species we are making the prediction for.
            c.	Take weighted average of the similarity scores, weighing them by the rating the user gave them (not applicable)
        """
        index = trainset[trainset['species_id'] == id].index.values
        # Fetch similarity between predictant species
        #print(self.similarities[index][0])

        similarity_scores = list(enumerate(similarities[index][0]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        #similarity_scores = similarity_scores[0:15]
        #print("similarity_scores: ",similarity_scores)

        # Include popularity of species
        similarity_total = []
        for item in similarity_scores:
            similarity_total.append(item)
            #print(item)
            if trainset.iloc[item[0]]['popular'] == 1:
                similarity_total.append((item[0],item[1]+1))

        similarity_total = sorted(similarity_total, key=lambda x: x[1], reverse=True)
        #print("similarity_total: ",similarity_total)

        similarity_total = similarity_total[0:15]
        species_index = [i[0] for i in similarity_total]
        #print(species_index)
        return species_index

def save_model(model):
    pickle.dump(model, open('CB_model_2.pkl', 'wb'))

def get_growth_habit(df):
        growth_habit = defaultdict(list)
        growth_habit_ids = defaultdict(int)
        max_id = 0
        for i in range(len(df)):
            species_id = df['species_id'][i]
            habit_list = df['growth_habit'][i].split('|')
            habit_id_list = []
            for habit in habit_list:
                habit = habit.strip()
                if habit == "":
                    continue
                else:
                    if habit in growth_habit_ids:
                        habit_id = growth_habit_ids[habit]
                    else:
                        habit_id = max_id
                        growth_habit_ids[habit] = habit_id
                        max_id += 1
                    habit_id_list.append(habit_id)
            growth_habit[species_id] = habit_id_list

        # Convert integer-encoded genre lists to bitfields that we can treat as vectors
        for (species_id, habit_id_list) in growth_habit.items():
            bitfield = [0] * max_id
            for habit_id in habit_id_list:
                bitfield[habit_id] = 1
            growth_habit[species_id] = bitfield
        return growth_habit

def get_native_place(df):
    native_place = defaultdict(list)
    native_place_ids = defaultdict(int)
    max_id = 0
    for i in range(len(df)):
        species_id = df['species_id'][i]
        native_list = df['native'][i].split('|')
        native_id_list = []
        for native in native_list:
            native =native.strip()
            if native == "":
                continue
            else:
                if native in native_place_ids:
                    native_id = native_place_ids[native]
                else:
                    native_id = max_id
                    native_place_ids[native] = native_id
                    max_id += 1
                native_id_list.append(native_id)
        native_place[species_id] = native_id_list
        #print(species_id)
        #print(native_list)
    #print(native_place)
    #print(native_place_ids)
    #print(len(native_place_ids))

    # Convert integer-encoded genre lists to bitfields that we can treat as vectors
    for (species_id, native_id_list) in native_place.items():
        bitfield = [0] * max_id
        for native_id in native_id_list:
            bitfield[native_id] = 1
        native_place[species_id] = bitfield
    return native_place

def get_edible_parts(df):
    #df.info()

    edible_parts = defaultdict(list)
    edible_parts_ids = defaultdict(int)
    max_id = 0
    for i in range(len(df)):
        species_id = df['species_id'][i]
        #print(df['edible_parts'][i])
        edible_list = df['edible_parts'][i].split('|')
        edible_id_list = []
        for edible in edible_list:
            edible =edible.strip()
            if edible == "":
                continue
            else:
                if edible in edible_parts_ids:
                    edible_id = edible_parts_ids[edible]
                else:
                    edible_id = max_id
                    edible_parts_ids[edible] = edible_id
                    max_id += 1
                edible_id_list.append(edible_id)
        edible_parts [species_id] = edible_id_list
        #print(species_id)
        #print(edible_list)
    #print(edible_parts)
    #print(edible_parts_ids)
    #print(len(edible_parts_ids))

    # Convert integer-encoded genre lists to bitfields that we can treat as vectors
    for (species_id, edible_id_list) in edible_parts.items():
        bitfield = [0] * max_id
        for edible_id in edible_id_list:
            bitfield[edible_id] = 1
        edible_parts[species_id] = bitfield
    #print(edible_parts)
    return edible_parts

def main():
        data = load_dataset()
        #print(growth_habit)
        algo = Content_Based_KNN()
        print("Done...")

        algo.fit(data)
        #prediction = algo.estimate(187414,data)
        #print(prediction)
        #save_model(algo)


if __name__ == "__main__":
    main()
