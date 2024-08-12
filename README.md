# End-to-End Text Summarization Project

## Setting Up the Environment

1. Create a virtual environment and install the required packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install .
```

> **Note:** The application needs to be installed as a package to run properly. If you prefer to run it without installing the package, you'll need to modify the `import` statements. For guidance, refer to this [Stack Overflow answer](https://stackoverflow.com/questions/76932293/why-do-i-keep-getting-modulenotfounderror-no-module-named-src).

## Model Training

To train the model, execute the following command:

```bash
python src/pipeline/train_model.py
```

After training the model, start the web application using one of these commands:

```bash
flask app
```

or

```bash
python app.py
```

## Contributing

Contributions are welcome! If you find any issues or want to add new features, feel free to submit a pull request.

## Contact Me

<table>
  <tr>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/instagram.png" alt="Instagram" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/twitter.png" alt="Twitter" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/github.png" alt="GitHub" width="50" height="50"></td>
    <td><img src="https://github.com/realsanjeev/protfolio/blob/main/src/assets/images/linkedin-logo.png" alt="LinkedIn" width="50" height="50"></td>
  </tr>
</table>

## License

This project is licensed under the [MIT License].

---

Feel free to modify and enhance this `README.md` as needed to match your specific project details. The provided steps are generic, and you should customize them according to the actual setup and configuration of your "Text Summarization end-to-end project" project.
