VAM Image Downloader
====================

1. Open Terminal and navigate to the extracted script folder.
   e.g.: cd /path/to/download_script/
   * Set permissions to the script file. e.g.: chmod +x vam_image_downloader.py
   (you need to do this only once!)

2. a) You can select from different search types:
      -o (objectnamesearch) e.g. -o "teapot"
      -m (materialsearch) e.g. -m "Brass, Nickel, Silver alloy, Silver-gilt"
	
   b) Create your command:
      ./vam_image_downloader.py -o "teapot" -m "Brass, Nickel, Silver alloy, Silver-gilt"

   c) Execute your command.

3. Script will create image folder and download all images to said folder.

4. It's optional to specify a folder name. So if you execute ./vam_image_downloader.py -d "example" all images will be downloaded to the specified folder.
   (important: add the "" in your command if you specify the folder)

5. Enjoy!

6. You can always type .vam_image_downloader.py -h for help.

7. Questions? Write me at bastian@ch3rr1.me
