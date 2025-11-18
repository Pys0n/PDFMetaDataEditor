# Python PDF Metadata Editor

## Requirements

The requirements for this project are: pypdf, dotenv

You can install them using this command:

```
pip install pypdf dotenv
```

## How to use the Editor

At first, run the `pdf.py` file:

```
python3 pdf.py
```

You can optionally add the path of your pdf-file to the command:

```
python3 pdf.py path_to_file.pdf
```
If the file is in the same directory as the python script, you can only write the pdf-file's name without the full path.

After you have start the script you will see something like this:

```
Filename..........my_pdf.pdf

/CreationDate.....D:20240107170843+01'00'   [2024-01-07 17:08:43]
/Creator..........Writer
/Producer.........LibreOffice 7.6

---------- Menu ----------

 [A]dd   [E]dit   [D]elete

 [Q]uit

 > 
```

Now you can add, edit or delete the metadata keys and their values.

### Useful Information

If you were asked to input the metadata key, you don't need to write the "/" at the beginning.

In additon, you don't need to write the full name of the key if the key is already unique:

```
Filename..........my_pdf.pdf

/CreationDate.....D:20240107170843+01'00'   [2024-01-07 17:08:43]
/Creator..........Writer
/Producer.........LibreOffice 7.6

--------------------------

Metadata Key  : Creat
```
"Creat" is not unique, because there are "**Creat**ionDate" and "**Creat**or", but "Creato" and "Creati" are unique. So if you want to change the creatin date you only need to write "Creati" instead of "/CreationDate".