using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace datasetCleaner
{
    class MainClass
    {
        static int datetime = 0;
        static int browser_language = 1;
        static int device_id = 2;
        static int device_first_seen = 3;
        static int os = 4;
        static int os_anomaly = 5;
        static int ua_os = 6;
        static int browser_language_anomaly = 7;
        static int fuzzy_device_id = 8;
        static int fuzzy_device_first_seen = 9;
        static int true_ip = 10;
        static int true_ip_geo = 11;
        static int proxy_ip = 12;
        static int proxy_ip_geo = 13;
        static int page_time_on = 14;
        static int transaction_amount = 15;
        static int frd = 16;


        public static void Main(string[] args)
        {
            //read input files
			string inputFileName = "ff24d96c-c22b-4449-b6cc-151d31e8619f_all.csv";
			FileStream inputFileStream = new FileStream(inputFileName, FileMode.Open, FileAccess.Read);
			StreamReader inputFileReader = new StreamReader(inputFileStream);

            string outputFileName = "cleaned_dataset.csv";
            FileStream outputFileStream = new FileStream(outputFileName, FileMode.Create, FileAccess.Write);
			StreamWriter outputFileWriter = new StreamWriter(outputFileStream);

            //skip header section
            outputFileWriter.WriteLine(inputFileReader.ReadLine());

            int lineCount = 0;

            //for each entry
			while (!inputFileReader.EndOfStream)
			{
				string inputLine = inputFileReader.ReadLine();
                List<string> inputCols = new List<string>(inputLine.Split(','));

                for (int i = 0; i < inputCols.Count; i++)
                {
                    if ( inputCols[i].Length > 0 && inputCols[i][0] == '\"' )
                    {
                        //dealing with a string
                        StringBuilder stringObj = new StringBuilder(inputCols[i]);

                        while(inputCols[i + 1][inputCols[i + 1].Length - 1] != '\"')
                        {
                            stringObj.Append( "," + inputCols[i + 1]);
                            inputCols.RemoveAt(i + 1);
                        }
                        //remove the last one as well
                        stringObj.Append("," + inputCols[i + 1]);
                        inputCols.RemoveAt(i + 1);

                        inputCols.RemoveAt(i);
                        inputCols.Insert(i,stringObj.ToString());
                    }
                }

                //datetime - convert to unix timestamp
                if(inputCols[datetime] != "")
                {
                    inputCols[datetime] = GetEpochFromDateString(inputCols[datetime]).ToString();
                }

                //browser_language - only consider the primary lanuage
                if(inputCols[browser_language] != "")
                {
                    string temp = inputCols[browser_language];
                    inputCols[browser_language] = inputCols[browser_language].Split(',')[0];

                    //remove \" at the front if it is there
                    if(inputCols[browser_language][0] == '\"')
                    {
                        inputCols[browser_language] = inputCols[browser_language].Substring(1);
                    }
                }

                //device_id - covert from hex to a unique number
                if(inputCols[device_id] != "")
                {
                    inputCols[device_id] = HexStringToInt(inputCols[device_id]).ToString();
                }

				//device_first_seen
				if (inputCols[device_first_seen] != "")
				{
					inputCols[device_first_seen] = GetEpochFromDateString(inputCols[device_first_seen]).ToString();
				}

				//fuzzy_device_id
				//device_id - covert from hex to a unique number
				if (inputCols[fuzzy_device_id] != "")
				{
					inputCols[fuzzy_device_id] = HexStringToInt(inputCols[fuzzy_device_id]).ToString();
				}

				//fuzzy_device_first_seen
				if (inputCols[fuzzy_device_first_seen] != "")
				{
					inputCols[fuzzy_device_first_seen] = GetEpochFromDateString(inputCols[fuzzy_device_first_seen]).ToString();
				}



                string outputLine = ArrayToCsvString(inputCols.ToArray());
                outputFileWriter.WriteLine(outputLine);

                lineCount++;
                if(lineCount % 10000 == 0)
                {
                    Console.WriteLine(lineCount);
                }
			}

			//close files
			outputFileWriter.Flush();
            outputFileWriter.Close();
			inputFileReader.Close();
        }

        public static int HexStringToInt(string hex)
        {
            string hexString = hex.ToUpper();

            //for the size of the dataset we only need to use 7 charactors to make the change of collision small
            int maxHexLength = 7;
            int start = Math.Min(0, hexString.Length - maxHexLength);
            string subHex = hexString.Substring(start, maxHexLength);
            return (int)Convert.ToUInt32(subHex, 16);
        }

        public static int GetEpochFromDateString(string entry)
        {
			string[] dateTimeParts = entry.Split(' ');
			string date = dateTimeParts[0];
			string[] dateParts = date.Split('-');
			int day = int.Parse(dateParts[2]);
			int month = int.Parse(dateParts[1]);
			int year = int.Parse(dateParts[0]);

			string[] timeParts = dateTimeParts[1].Split(':');
			int hour = int.Parse(timeParts[0]);
			int minute = int.Parse(timeParts[1]);
            int second = (int)float.Parse(timeParts[2]);

			DateTime DateTimeObj = new DateTime(year, month, day, hour, minute, second, DateTimeKind.Utc);
            int unixTimeStamp = (int)(DateTimeObj.Subtract(new DateTime(1970, 1, 1))).TotalSeconds;

            return unixTimeStamp;
		}

        public static string ArrayToCsvString(string[] array)
        {
            StringBuilder returnString = new StringBuilder();

            for (int i = 0; i < array.Length - 1; i++)
            {
                returnString.Append(array[i] + ",");
            }
            returnString.Append(array[array.Length - 1]);
            return returnString.ToString();
        }
    }
}
