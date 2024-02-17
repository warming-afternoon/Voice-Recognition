from pydub import AudioSegment
from noisereduce import reduce_noise
 
# 使用pydub加载.wav文件
audio = AudioSegment.from_wav("input.wav")
 
# 将音频转换为numpy数组
audio_array = audio.get_array_of_samples()
 
# 对音频数组执行降噪
reduced_noise = reduce_noise(audio_array, audio.frame_rate)
 
# 从降噪数组创建新的AudioSgment
reduced_audio = AudioSegment(
    reduced_noise.tobytes(),
    frame_rate=audio.frame_rate,
    sample_width=audio.sample_width,
    channels=audio.channels
)
 
# 将降噪音频导出为.wav文件
reduced_audio.export("output.wav", format="wav")