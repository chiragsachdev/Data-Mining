#!/usr/bin/python3
import random, sys, pickle, math, os
import numpy as np, pandas as pd, scipy.spatial
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

# get chi value: log(maxval- minval)/minval
def ft_getchi(maxval, minval):
	if minval == 0:
		return (None)
	chi = math.log((maxval - minval)/minval)

	return (chi)

# creates a n d-dimensional points in a dataframe and calculates the euclicdian distance
def ft_create_points(n, d):
	data=[]
	for i in range(n):
		data.append([round(random.random()*100, 3) for _ in range(d)])
	return (data)

# get the chi value for given valoe of d and n
def ft_getinstancechi(rows, cols):
	data=ft_create_points(rows, cols)
	df=pd.DataFrame(data)
	# print(df)
	dist_m_e=pd.DataFrame(scipy.spatial.distance.cdist(df.values, df.values, metric="euclidean"))
	np.fill_diagonal(dist_m_e.values,None)
	max_dist_e = dist_m_e.max().max()
	min_dist_e = dist_m_e.min().min()
	e_chi = ft_getchi(max_dist_e, min_dist_e)
	
	dist_m_m=pd.DataFrame(scipy.spatial.distance.cdist(df.values, df.values, metric="cityblock"))
	np.fill_diagonal(dist_m_m.values,None)
	max_dist_m = dist_m_m.max().max()
	min_dist_m = dist_m_m.min().min()
	m_chi=ft_getchi(max_dist_m, min_dist_m)

	return([e_chi, m_chi])

# plotting the place of n,d,chi based on euclidean distance
def ft_plotplane_e(df):
	fig = plt.figure()
	ax=fig.gca(projection='3d')
	ax.plot_trisurf(df["d"], df["n"], df["Chi-Euclidian"],linewidth=0.1, antialiased=True, cmap="jet", edgecolor=None)
	ax.set_ylabel("n",fontsize=20)
	ax.set_xlabel("d",fontsize=20)
	ax.set_zlabel(r"$\chi$",fontsize=20)
	plt.savefig("euclidean.pdf", bbox_inches='tight')
	# plt.show()

# plotting the place of n,d,chi based on manhattan distance
def ft_plotplane_m(df):
	fig = plt.figure()
	ax=fig.gca(projection='3d')
	ax.plot_trisurf(df["d"], df["n"], df["Chi-Manhattan"],linewidth=0.1, cmap="hsv")
	ax.set_ylabel(r"$n$",fontsize=20)
	ax.set_xlabel(r"$d$",fontsize=20)
	ax.set_zlabel(r"$\chi$")
	plt.savefig("manhattan.pdf", bbox_inches='tight')

def main():
	chi_df=None	
	if(os.path.isfile("chi_df.csv")):
		chi_df=pd.read_csv("./chi_df.csv")
	else:
		chi_df={"n":[], "d":[], "Chi-Euclidian":[], "Chi-Manhattan":[]}
		for i in range(100, 1001):
			print(i,'...')
			for j in range(1, 101):
				chi_s=ft_getinstancechi(i,j)
				chi_df["n"].append(i)
				chi_df["d"].append(j)
				chi_df["Chi-Euclidian"].append(chi_s[0])
				chi_df["Chi-Manhattan"].append(chi_s[1])
		chi_df=pd.DataFrame(chi_df)
		chi_df.to_csv("./chi_df.csv")

	ft_plotplane_e(chi_df)
	ft_plotplane_m(chi_df)

if __name__=="__main__":
	main()