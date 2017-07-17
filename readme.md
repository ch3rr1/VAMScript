# Victoria and Albert Museum Catalog Script

1. Open Terminal and navigate to the folder where you placed the script.
e.g.: `cd /path/to/script/`
   
   Set permissions to the script file. e.g.: `chmod +x vam_script.py`
   
   (You need to do this only once!)

2. You can select from different search types:
  
   -q `--query "teapot"`

   -n `--namesearch "Van Gogh"`

   -o `--objectnamesearch "teapot"`
   
   -m `--materialsearch "Brass, Nickel, Silver alloy, Silver-gilt"`
   
   -p `--placesearch "France"`

   -b `--before "-220"`

   -a `--after "1516"`

   Create your command: `./vam_script.py -q "teapot" -m "brass, nickel, silver alloy, silver-gilt"`

   Execute your command.

3. Script will create image folder and download all images to said folder.
   
   A info file with all the image information gets generated and placed in the folder.

   A json file set (for every query) gets generaten and is placed in the image folder under.

4. It's optional to specify a folder name. So if you execute `./vam_script.py -d "example"` all images will be downloaded to the specified folder.
   
   (Important: add the "" in your command if you specify the folder)

5. Enjoy!

6. You can always type `./vam_script.py -h` for help.

7. Questions? bastian@ch3rr1.me
