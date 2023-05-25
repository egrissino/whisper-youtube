'''
Whisper Youtube
'''


'''
Check for Installed packages
'''

import sys
import warnings
import whisper
from pathlib import Path
import yt_dlp
import subprocess
import torch
import shutil
import numpy as np
import SeleniumYT as syt

def loadModel():
    """
    """
    global Model
    device = torch.device('cuda:0')
    print('Using device:', device, file=sys.stderr)
         

    #@markdown # **Model selection** 🧠
    #@markdown As of the first public release, there are 4 pre-trained options to play with:
    #@markdown |  Size  | Parameters | English-only model | Multilingual model | Required VRAM | Relative speed |
    #@markdown |:------:|:----------:|:------------------:|:------------------:|:-------------:|:--------------:|
    #@markdown |  tiny  |    39 M    |     `tiny.en`      |       `tiny`       |     ~1 GB     |      ~32x      |
    #@markdown |  base  |    74 M    |     `base.en`      |       `base`       |     ~1 GB     |      ~16x      |
    #@markdown | small  |   244 M    |     `small.en`     |      `small`       |     ~2 GB     |      ~6x       |
    #@markdown | medium |   769 M    |    `medium.en`     |      `medium`      |     ~5 GB     |      ~2x       |
    #@markdown | large  |   1550 M   |        N/A         |      `large`       |    ~10 GB     |       1x       |

    #@markdown ---
    Model = 'tiny.en' #@param ['tiny.en', 'tiny', 'base.en', 'base', 'small.en', 'small', 'medium.en', 'medium', 'large']
    #@markdown ---
    #@markdown **Run this cell again if you change the model.**

    whisper_model = whisper.load_model(Model)

    if Model in whisper.available_models():
        print(f"**{Model} model is selected.**")
    else:
        print(f"**{Model} model is no longer available.** Please select one of the following: - {' - '.join(whisper.available_models())}")

    return whisper_model
         

def downloadVideo(URL):
    """
    """
    global video_path_local_list
    #URL = "https://www.youtube.com/watch?v=ED_yPDdqG5Y" #@param {type:"string"}
    video_path = "/my_video.mp4" #@param {type:"string"}

    video_path_local_list = []


    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
        'postprocessors': [{  # Extract audio using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download([URL])
        list_video_info = [ydl.extract_info(URL, download=False)]
        
    for video_info in list_video_info:
        video_path_local_list.append(Path(f"{video_info['id']}.wav"))

    for video_path_local in video_path_local_list:
        if video_path_local.suffix == ".mp4":
            video_path_local = video_path_local.with_suffix(".wav")
            result  = subprocess.run(["ffmpeg", "-i", str(video_path_local.with_suffix(".mp4")), "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", str(video_path_local)])

def getTranscript(whisper_model):

    #@markdown # **Run the model** 🚀
    #@markdown Run this cell to execute the transcription of the video. This can take a while and very based on the length of the video and the number of parameters of the model selected above.
    #@markdown ## **Parameters** ⚙️
    #@markdown ### **Behavior control**
    #@markdown ---
    language = "English" #@param ['Auto detection', 'Afrikaans', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 'Assamese', 'Azerbaijani', 'Bashkir', 'Basque', 'Belarusian', 'Bengali', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Castilian', 'Catalan', 'Chinese', 'Croatian', 'Czech', 'Danish', 'Dutch', 'English', 'Estonian', 'Faroese', 'Finnish', 'Flemish', 'French', 'Galician', 'Georgian', 'German', 'Greek', 'Gujarati', 'Haitian', 'Haitian Creole', 'Hausa', 'Hawaiian', 'Hebrew', 'Hindi', 'Hungarian', 'Icelandic', 'Indonesian', 'Italian', 'Japanese', 'Javanese', 'Kannada', 'Kazakh', 'Khmer', 'Korean', 'Lao', 'Latin', 'Latvian', 'Letzeburgesch', 'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese', 'Maori', 'Marathi', 'Moldavian', 'Moldovan', 'Mongolian', 'Myanmar', 'Nepali', 'Norwegian', 'Nynorsk', 'Occitan', 'Panjabi', 'Pashto', 'Persian', 'Polish', 'Portuguese', 'Punjabi', 'Pushto', 'Romanian', 'Russian', 'Sanskrit', 'Serbian', 'Shona', 'Sindhi', 'Sinhala', 'Sinhalese', 'Slovak', 'Slovenian', 'Somali', 'Spanish', 'Sundanese', 'Swahili', 'Swedish', 'Tagalog', 'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Turkish', 'Turkmen', 'Ukrainian', 'Urdu', 'Uzbek', 'Valencian', 'Vietnamese', 'Welsh', 'Yiddish', 'Yoruba']
    #@markdown > Language spoken in the audio, use `Auto detection` to let Whisper detect the language.
    
    verbose = 'Progress bar' # ['Live transcription', 'Progress bar', 'None']
    #@markdown > Whether to print out the progress and debug messages.

    output_format = 'txt' # ['txt', 'vtt', 'srt', 'tsv', 'json', 'all']
    # Type of file to generate to record the transcription.

    task = 'transcribe' #['transcribe', 'translate']
    # Whether to perform X->X speech recognition (`transcribe`) or X->English translation (`translate`).

    # **Optional: Fine tunning** 

    temperature = 0.15
    # Temperature to use for sampling.

    temperature_increment_on_fallback = 0.2
    # Temperature to increase when falling back when the decoding fails to meet either of the thresholds below.

    best_of = 5
    # Number of candidates when sampling with non-zero temperature.

    beam_size = 8
    # Number of beams in beam search, only applicable when temperature is zero.
    
    patience = 1.0
    #@markdown > Optional patience value to use in beam decoding, as in [*Beam Decoding with Controlled Patience*](https://arxiv.org/abs/2204.05424), the default (1.0) is equivalent to conventional beam search.

    length_penalty = -0.05
    #@markdown > Optional token length penalty coefficient (alpha) as in [*Google's Neural Machine Translation System*](https://arxiv.org/abs/1609.08144), set to negative value to uses simple length normalization.

    suppress_tokens = "-1"
    #> Comma-separated list of token ids to suppress during sampling; '-1' will suppress most special characters except common punctuations.

    initial_prompt = ""
    #> Optional text to provide as a prompt for the first window.

    condition_on_previous_text = True
    #> if True, provide the previous output of the model as a prompt for the next window; disabling may make the text inconsistent across windows, but the model becomes less prone to getting stuck in a failure loop.
    fp16 = True
    
    compression_ratio_threshold = 2.4
    # If the gzip compression ratio is higher than this value, treat the decoding as failed.

    logprob_threshold = -1.0
    # If the average log probability is lower than this value, treat the decoding as failed.

    no_speech_threshold = 0.6
    # If the probability of the <|nospeech|> token is higher than this value AND the decoding has failed due to `logprob_threshold`, consider the segment as silence.


    verbose_lut = {
        'Live transcription': True,
        'Progress bar': False,
        'None': None
    }

    args = dict(
        language = (None if language == "Auto detection" else language),
        verbose = verbose_lut[verbose],
        task = task,
        temperature = temperature,
        temperature_increment_on_fallback = temperature_increment_on_fallback,
        best_of = best_of,
        beam_size = beam_size,
        patience=patience,
        length_penalty=(length_penalty if length_penalty>=0.0 else None),
        suppress_tokens=suppress_tokens,
        initial_prompt=(None if not initial_prompt else initial_prompt),
        condition_on_previous_text=condition_on_previous_text,
        fp16=fp16,
        compression_ratio_threshold=compression_ratio_threshold,
        logprob_threshold=logprob_threshold,
        no_speech_threshold=no_speech_threshold
    )

    temperature = args.pop("temperature")
    temperature_increment_on_fallback = args.pop("temperature_increment_on_fallback")
    if temperature_increment_on_fallback is not None:
        temperature = tuple(np.arange(temperature, 1.0 + 1e-6, temperature_increment_on_fallback))
    else:
        temperature = [temperature]

    if Model.endswith(".en") and args["language"] not in {"en", "English"}:
        warnings.warn(f"{Model} is an English-only model but receipted '{args['language']}'; using English instead.")
        args["language"] = "en"

    for video_path_local in video_path_local_list:
        print(f"### {video_path_local}")

        video_transcription = whisper.transcribe(
            whisper_model,
            str(video_path_local),
            temperature=temperature,
            **args,
        )

        # Save output
        whisper.utils.get_writer(
            output_format=output_format,
            output_dir=video_path_local.parent
        )(
            video_transcription,
            str(video_path_local.stem),
            options=dict(
                highlight_words=False,
                max_line_count=None,
                max_line_width=None,
            )
        )

        #yield video_transcription



if __name__ == "__main__":

    URL = "https://www.youtube.com/watch?v=FV7pW4p60VI"

    print("Getting Youtube Transcript")
    setup()
    syt = syt.getTranscription(URL)

    print("Genertaing Text from Whisper")
    model = loadModel()
    downloadVideo(URL)
    
    wyt = getTranscript(model)


    

    
