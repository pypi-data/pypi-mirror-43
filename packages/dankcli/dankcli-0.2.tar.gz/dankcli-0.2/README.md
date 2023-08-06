This is a CLI Meme Generator which automatically adds white space and text to the top of your image.

## Usage

```
$ python -m dankcli 'path/to/image' 'Text you want need'
```

The text gets automatically wrapped according to width of image but you can also have intentional \n in your text.
The meme is saved in a new folder called 'dankcli-output' with a name 'meme%s.png'

## Example

```
$ python -m dankcli 'templates/reality.png' 'When you learn how to inspect element in chrome'
```
