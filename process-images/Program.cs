using System;
using System.IO;
using System.Drawing.Imaging;
using System.Drawing;
using System.Linq;
using System.Collections.Generic;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {

            const string RESULTS_PATH = @"C:\Users\ag4488\Documents\Visual Studio 2019\Projects\Machine Learning\Image Processing\ImageEditor\GenerateCorruptImage\Results";

            //=== Example of 2-dimensional array saved as image ===========================================
            // Create 2D array of integers
            int width = 320;
            int height = 240;
            int stride = width * 4;
            int[,] integers = new int[width, height];

            // Fill array with random values
            Random random = new Random();
            for (int x = 0; x < width; ++x)
            {
                for (int y = 0; y < height; ++y)
                {
                    byte[] bgra = new byte[] { (byte)random.Next(255), (byte)random.Next(255), (byte)random.Next(255), 255 };
                    integers[x, y] = BitConverter.ToInt32(bgra, 0);
                }
            }

            // Copy into bitmap
            Bitmap bitmap;
            unsafe
            {
                fixed (int* intPtr = &integers[0, 0])
                {
                    bitmap = new Bitmap(width, height, stride, PixelFormat.Format32bppRgb, new IntPtr(intPtr));
                }
                bitmap.Save($"{RESULTS_PATH}\\example_dataset_to_img.png", ImageFormat.Png);
            }

            //=== Wine dataset array saved as image ===========================================
            var lines = File.ReadAllLines("winequality.csv").ToList<string>();
            List<int[]> lwineds = new List<int[]>();
            foreach (var line in lines)
            {
                var iline = new int[12];
                int i = 0;
                foreach (var elem in line.Split(',').ToList())
                    iline[i++] = int.Parse(elem);
                lwineds.Add(iline);
            }
            var xwineds = lwineds.ToArray();

            // transform original, uncorrupted wine dataset to bitmap image
            Bitmap grayScale = new Bitmap(xwineds[0].Length, xwineds.Length);
            for (Int32 x = 0; x < grayScale.Height; x++)
                for (Int32 y = 0; y < grayScale.Width; y++)
                {
                    Int32 gs = xwineds[x][y];

                    grayScale.SetPixel(y,x, Color.FromArgb(gs, gs, gs));
                }
            grayScale.Save($"{RESULTS_PATH}\\wine_dataset_img_original.png", ImageFormat.Png);

            //=== Insert random nulls in Wine dataset image ==================================
            for (int i = 0; i < 300; i++)
                PickRandom(xwineds);
            grayScale = new Bitmap(xwineds[0].Length, xwineds.Length);
            for (Int32 x = 0; x < grayScale.Height; x++)
                for (Int32 y = 0; y < grayScale.Width; y++)
                {
                    Int32 gs = xwineds[x][y];
                    if (gs < 0)
                        grayScale.SetPixel(y, x, Color.FromArgb(255, 0, 0));
                    else
                        grayScale.SetPixel(y, x, Color.FromArgb(gs, gs, gs));
                }
            grayScale.Save($"{RESULTS_PATH}\\wine_dataset_img_corrupt.png", ImageFormat.Png);
        }

        static Random Rand = null;

        public static void PickRandom(int[][] values)
        {
            // Create the Random object if it doesn't exist.
            if (Rand == null) Rand = new Random();

            // Pick an item and return it.
            var x = Rand.Next(0, values.Length);
            var y = Rand.Next(0, 11);
            values[x][y] = -1;
        }
    }
}
