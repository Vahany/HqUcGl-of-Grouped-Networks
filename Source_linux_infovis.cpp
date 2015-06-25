// -------------------------------------------------------------- -*- C++ -*-
// Version 12.6.1  
// --------------------------------------------------------------------------
// Licensed Materials - Property of IBM
// 5725-A06 5725-A29 5724-Y48 5724-Y49 5724-Y54 5724-Y55 5655-Y21
// Copyright IBM Corporation 2000, 2014. All Rights Reserved.
//
// US Government Users Restricted Rights - Use, duplication or
// disclosure restricted by GSA ADP Schedule Contract with
// IBM Corp.
// --------------------------------------------------------------------------

#include <ilcplex/ilocplex.h>
#include <ilopl/iloopl.h>
#include <ilopl/ilooplprofiler.h>
#include <vector>	
#include <iostream>
#include <fstream>
#include <string>
#include <math.h>

double GetTickCount(void)
{
	time_t timev;
	return time(&timev);
}

void printValues(IloEnv env, IloCplex cplex, IloNumVarArray var, IloNumArray val)
{
	//print values
	std::vector<string> vxs;
	std::vector<string> vys;
	std::vector<string> vwd;
	std::vector<string> vht;
	//added for correct ordering
	std::vector<string> vnxs;
	std::vector<string> vnys;
	std::vector<string> vnwd;
	std::vector<string> vnht;
	//objectives
	string vmystress;
	string vmysize;
	string vmymaxX;
	string vmymaxY;
	string vmycenter;
	for (int i = 0; i < var.getSize(); i++)
	{
		std::string str1 = var[i].getName();
		if (str1.compare(0, 2, "xs") == 0) {
			vxs.push_back(to_string(val[i]));
			//added for correct ordering
			unsigned startposition = str1.find_first_of("(");
			vnxs.push_back(str1.substr(startposition + 1, str1.find_last_of(")") - startposition - 1));
		}
		else if (str1.compare(0, 2, "ys") == 0) {
			vys.push_back(to_string(val[i]));
			unsigned startposition = str1.find_first_of("(");
			vnys.push_back(str1.substr(startposition + 1, str1.find_last_of(")") - startposition - 1));
		}
		else if (str1.compare(0, 2, "wd") == 0){
			vwd.push_back(to_string(val[i]));
			unsigned startposition = str1.find_first_of("(");
			vnwd.push_back(str1.substr(startposition + 1, str1.find_last_of(")") - startposition - 1));
		}
		else if (str1.compare(0, 2, "ht") == 0){
			vht.push_back(to_string(val[i]));
			unsigned startposition = str1.find_first_of("(");
			vnht.push_back(str1.substr(startposition + 1, str1.find_last_of(")") - startposition - 1));
		}
		else if (str1.compare(0, 9, "thestress") == 0){
			vmystress = to_string(val[i]);
		}
		else if (str1.compare(0, 7, "thesize") == 0){
			vmysize = to_string(val[i]);
		}
		else if (str1.compare(0, 4, "maxX") == 0){
			vmymaxX = to_string(val[i]);
		}
		else if (str1.compare(0, 4, "maxY") == 0){
			vmymaxY = to_string(val[i]);
		}
		else if (str1.compare(0, 9, "thecenter") == 0){
			vmycenter = to_string(val[i]);
		}
	}
	int mysize = vxs.size();
	//added for correct ordering
	int mytotal = 0;
	string mytmp;
	while (mytotal < mysize) {
		for (int i = 0; i < mysize; i++){
			if (vnxs[i] == to_string(mytotal + 1)){
				mytmp = vxs[mytotal];
				vxs[mytotal] = vxs[i];
				vxs[i] = mytmp;

				vnxs[i] = vnxs[mytotal];
				vnxs[mytotal] = to_string(mytotal + 1);
			}
			if (vnys[i] == to_string(mytotal + 1)){
				mytmp = vys[mytotal];
				vys[mytotal] = vys[i];
				vys[i] = mytmp;

				vnys[i] = vnys[mytotal];
				vnys[mytotal] = to_string(mytotal + 1);
			}
			if (vnwd[i] == to_string(mytotal + 1)){

				mytmp = vwd[mytotal];
				vwd[mytotal] = vwd[i];
				vwd[i] = mytmp;

				vnwd[i] = vnwd[mytotal];
				vnwd[mytotal] = to_string(mytotal + 1);
			}
			if (vnht[i] == to_string(mytotal + 1)){
				mytmp = vht[mytotal];
				vht[mytotal] = vht[i];
				vht[i] = mytmp;

				vnht[i] = vnht[mytotal];
				vnht[mytotal] = to_string(mytotal + 1);
			}
		}
		mytotal++;
	}

	env.out() << "++++" << endl;
	env.out() << "#modules=" << endl;
	for (int i = 0; i < mysize; i++){
		env.out() << "Vertex" << i + 1 << ": x=" << vxs[i] << " y=" << vys[i] << " w=" << vwd[i] << " h=" << vht[i] << endl;
	}
	env.out() << "stress =" << vmystress << endl;
	env.out() << "size =" << vmysize << endl;
	env.out() << "maxX =" << vmymaxX << endl;
	env.out() << "maxY =" << vmymaxY << endl;
	env.out() << "center =" << vmycenter << endl;
	env.out() << "----------" << endl;
	env.out() << "==========" << endl;
	env.out() << "% Real Time: " << cplex.getCplexTime() << endl; //getCplexTime vs getTime
	env.out() << "% CPU Time: " << cplex.getDetTime() << endl;
	env.out() << "++++" << endl;
	//end print values
}

int
main(int argc, char **argv)
{
	int startTime = GetTickCount();
	IloEnv env;
	IloCplex cplex(env);
	cplex.setParam(IloCplex::ClockType,1);

	try {
		IloNumArray val(env);
		string myrelaxedline;
		
		int jsonconvtime = GetTickCount();
		string mydatfilename = argv[2];
		//get the number of nodes from the filename
		string mygraphsize = mydatfilename.substr(mydatfilename.find("/graph")+6,mydatfilename.find("_linux")-mydatfilename.find("/graph")-6);
		int mytimelimit = round(stoi(mygraphsize)/5);
		string myfilename = mydatfilename.substr(0, mydatfilename.size() - 4);
		//convert .json to .dat file
		string mycommand = string() + "python conv_json2dzn_infovis.py " + myfilename + ".json ordered";
		system(mycommand.c_str());
		env.out() << "json conv time : " << to_string(GetTickCount() - jsonconvtime) << endl;

		int compiletime = GetTickCount();
			IloOplRunConfiguration rc;
			IloOplModel opl;
			IloOplSettings settings;
			IloOplErrorHandler handler;

			rc = IloOplRunConfiguration(env, argv[1], argv[2]);
			handler = rc.getErrorHandler();
			opl = rc.getOplModel();
			settings = opl.getSettings();
			settings.setWithLocations(IloTrue);
			settings.setWithNames(IloTrue);
			settings.setForceElementUsage(IloTrue);
			opl.generate();
			opl.getCplex().exportModel("current.mps");
			env.out() << "compiling model time : " << to_string(GetTickCount() - compiletime) << endl;

			int importtime = GetTickCount();
			IloModel model(env);
			IloObjective   obj;
			IloNumVarArray var(env);
			IloRangeArray  rng(env);

			cplex.importModel(model, "current.mps", obj, var, rng);
			cplex.extract(model);
			env.out() << "import model time : " << to_string(GetTickCount() - importtime) << endl;
			
			cplex.setParam(IloCplex::Threads, 1);
			cplex.solve();
			val.clear();
			cplex.getValues(val, var);

			int printingtime = GetTickCount();
			printValues(env, cplex, var, val);
			env.out() << "printing time : "<<to_string(GetTickCount() - printingtime) << endl;

			bool addmipstart = true;
			bool myrelaxedfirst= true;	

			ifstream infile((myfilename+".groups.txt"));

			vector<string> myrelaxednodes;
			while (!infile.eof())
			{
				string myline;
				string mynodes;
				myrelaxednodes.clear();
				getline(infile, myline);

				stringstream myinline(myline);

				while (myinline.good()){
					string myvalue;
					getline(myinline, myvalue, ',');
					mynodes = mynodes + ' ' + myvalue;
					myrelaxednodes.push_back(myvalue);
				}

				if (myrelaxedfirst){
					myrelaxedline += "[" + myline + "]";
					myrelaxedfirst = false;
				}
				else
				{
					myrelaxedline += ",[" + myline + "]";

				}

				int deletetime = GetTickCount();

				IloRangeArray todelete(env);

				for (int i = 0; i < rng.getSize(); i++) //rng.getSize()
				{
					IloNumVarArray va(env);
					for (IloExpr::LinearIterator it = rng[i].getLinearIterator(); it.ok(); ++it) {
						IloNumVar v = it.getVar();
						va.add(v);
					}
					if (va.getSize() == 2)
					{
						string s1 = va[0].getName();
						string s2 = va[1].getName();

						string myxs;
						string myxf;
						string myys;
						string myyf;

						string mxs,mxf,mys,myf;

						for (int j = 0; j < myrelaxednodes.size(); j++){
							myxs = string() + "xs(" + myrelaxednodes[j] + ")";
							myxf = string() + "xf(" + myrelaxednodes[j] + ")";
							myys = string() + "ys(" + myrelaxednodes[j] + ")";
							myyf = string() + "yf(" + myrelaxednodes[j] + ")";

							mxs = string() + "xs#" + to_string(stoi(myrelaxednodes[j])-1);
							mxf = string() + "xf#" + to_string(stoi(myrelaxednodes[j])-1);
							mys = string() + "ys#" + to_string(stoi(myrelaxednodes[j])-1);
							myf = string() + "yf#" + to_string(stoi(myrelaxednodes[j])-1);
							if (((s1.compare(0, myrelaxednodes[j].size() + 4, myxs) == 0) && (s2.compare(0, 2, "xf") == 0)) ||
								((s1.compare(0, 2, "xf") == 0) && (s2.compare(0, myrelaxednodes[j].size() + 4, myxs) == 0)) ||
								((s1.compare(0, myrelaxednodes[j].size() + 4, myxf) == 0) && (s2.compare(0, 2, "xs") == 0)) ||
								((s1.compare(0, 2, "xs") == 0) && (s2.compare(0, myrelaxednodes[j].size() + 4, myxf) == 0)) ||
								((s1.compare(0, myrelaxednodes[j].size() + 4, myys) == 0) && (s2.compare(0, 2, "yf") == 0)) ||
								((s1.compare(0, 2, "yf") == 0) && (s2.compare(0, myrelaxednodes[j].size() + 4, myys) == 0)) ||
								((s1.compare(0, myrelaxednodes[j].size() + 4, myyf) == 0) && (s2.compare(0, 2, "ys") == 0)) ||
								((s1.compare(0, 2, "ys") == 0) && (s2.compare(0, myrelaxednodes[j].size() + 4, myyf) == 0))){
								env.out() << "old deleted "<< rng[i] << endl;
								todelete.add(rng[i]);
							}
							else
							if ( ((s1 == mxs) && (s2.compare(0, 2, "xf") == 0)) ||
								((s1.compare(0, 2, "xf") == 0) && (s2 == mxs)) ||
								((s1 == mxf) && (s2.compare(0, 2, "xs") == 0)) ||
								((s1.compare(0, 2, "xs") == 0) && (s2 == mxf)) ||
								((s1 == mys) && (s2.compare(0, 2, "yf") == 0)) ||
								((s1.compare(0, 2, "yf") == 0) && (s2 == mys)) ||
								((s1 == myf) && (s2.compare(0, 2, "ys") == 0)) ||
								((s1.compare(0, 2, "ys") == 0) && (s2 == myf))){
								
								env.out() << "new deleted "<< rng[i] << "the relaxed node "<< myrelaxednodes[j]<< ";;;;;";
								todelete.add(rng[i]);
							}
						}
					}
				}

				model.remove(todelete);
				todelete.end();
				env.out() << "deletion time : " << to_string(GetTickCount() - deletetime) << endl;

				string mystring;
				if (addmipstart){
					cplex.addMIPStart(var, val, cplex.MIPStartCheckFeas);
				}
				cplex.setParam(IloCplex::TiLim, mytimelimit);
				int solvingtime = GetTickCount();
				cplex.solve();
				env.out() << "solving time : " << to_string(GetTickCount() - solvingtime) << endl;
				int gettingvaltime = GetTickCount();
				if ((cplex.getStatus() == IloAlgorithm::Optimal) || (cplex.getStatus() == IloAlgorithm::Feasible)){
					val.clear();
					cplex.getValues(val, var);
					printValues(env, cplex, var, val);
					env.out() << "FEASIBLE " << cplex.getStatus() << endl;
					addmipstart = true;
				}
				else
				{
					env.out() << "INFEASIBLE " << cplex.getStatus() << endl;
					addmipstart = false;
				}
				env.out() << "getting val time : " << to_string(GetTickCount() - gettingvaltime) << endl;
				IloRangeArray myrng1(env);
				IloNumVar myvar1(env);
				IloNumVar myvar2(env);
				vector<string> myedges;
				for (int j = 0; j < myrelaxednodes.size(); j++){
					string myxs = string() + "xs(" + myrelaxednodes[j] + ")";
					string myxf = string() + "xf(" + myrelaxednodes[j] + ")";
					string myys = string() + "ys(" + myrelaxednodes[j] + ")";
					string myyf = string() + "yf(" + myrelaxednodes[j] + ")";

					string mxs = string() + "xs#"+ to_string(stoi(myrelaxednodes[j])-1);
					string mxf = string() + "xf#"+ to_string(stoi(myrelaxednodes[j])-1);
					string mys = string() + "ys#"+ to_string(stoi(myrelaxednodes[j])-1);
					string myf = string() + "yf#"+ to_string(stoi(myrelaxednodes[j])-1);
					
					int edgetime = GetTickCount();
					string mydist = string() + "dist#" + to_string(stoi(myrelaxednodes[j])-1);
					//get the edges from file, removed in later versions
					mycommand = string() + "python get_edges.py " + myfilename + ".json " + myrelaxednodes[j];
					system(mycommand.c_str());
					ifstream edgesinfile((myfilename + ".edges.txt"));
					
					myedges.clear();
					while (!infile.eof())
					{
						string edgesmyline;
						
						getline(edgesinfile, edgesmyline);
						if (edgesmyline == ""){
							break;
						}

						stringstream edgesmyinline(edgesmyline);

						while (edgesmyinline.good()){
							string edgesmyvalue;
							getline(edgesmyinline, edgesmyvalue, ',');
							myedges.push_back(edgesmyvalue);
						}
					}

					env.out() << "edge time : " << to_string(GetTickCount() - edgetime) << endl;

					int additiontime = GetTickCount();
					for (int i = 0; i < var.getSize(); i++)
					{
							
						string myvarname = var[i].getName();
						if (myvarname.compare(0, mydist.size(), mydist) == 0){
							for (int edy = 0; edy < myedges.size(); edy++){
								string mynewdist = mydist + "#" + to_string(stoi(myedges[edy]) - 1);
								if (myvarname==  mynewdist){
									myrng1.add(var[i] <= val[i]);
								}
							}
							
						}
						else
						if ((myvarname.compare(0, myxs.size(), myxs) == 0) || (myvarname == mxs))
						{
							myvar1 = var[i];
							for (int ii = 0; ii < var.getSize(); ii++)
							{
								myvarname = var[ii].getName();
								if ((myvarname.compare(0, 2, "xf") == 0) && (val[ii] <= val[i]))
								{
									myvar2 = var[ii];
									myrng1.add(-myvar1 + myvar2 <= 0);
								}
							}
						}
						else
							if ((myvarname.compare(0, myxf.size(), myxf) == 0) || (myvarname == mxf))
							{
							myvar1 = var[i];
							for (int ii = 0; ii < var.getSize(); ii++)
							{
								myvarname = var[ii].getName();
								if ((myvarname.compare(0, 2, "xs") == 0) && (val[i] <= val[ii]))
								{
									myvar2 = var[ii];
									myrng1.add(-myvar2 + myvar1 <= 0);
								}
							}
							}
							else
								if ((myvarname.compare(0, myys.size(), myys) == 0) || (myvarname == mys))
								{
							myvar1 = var[i];
							for (int ii = 0; ii < var.getSize(); ii++)
							{
								myvarname = var[ii].getName();
								if ((myvarname.compare(0, 2, "yf") == 0) && (val[ii] <= val[i]))
								{
									myvar2 = var[ii];
									myrng1.add(-myvar1 + myvar2 <= 0);
								}
							}
								}
								else
									if ((myvarname.compare(0, myyf.size(), myyf) == 0) || (myvarname == myf))
									{
							myvar1 = var[i];
							for (int ii = 0; ii < var.getSize(); ii++)
							{
								myvarname = var[ii].getName();
								if ((myvarname.compare(0, 2, "ys") == 0) && (val[i] <= val[ii]))
								{
									myvar2 = var[ii];
									myrng1.add(-myvar2 + myvar1 <= 0);
								}
							}
									}

					}
					env.out() << "addition time : " << to_string(GetTickCount() - additiontime) << endl;

				}
				model.add(myrng1);
				rng.add(myrng1);
				myrng1.end();
			}

			env.out() << "total time : " << to_string(GetTickCount() - jsonconvtime) << endl;
	}
	catch (IloException& e) {
		cerr << "Concert exception caught: " << e << endl;
	}
	catch (...) {
		cerr << "Unknown exception caught" << endl;
	}

	env.end();
	return 0;
} 
