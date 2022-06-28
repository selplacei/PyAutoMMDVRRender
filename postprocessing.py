# Implementations of several useful post-processing functions.
# See the comments in each function for instructions on how to apply them.
# All functions assume that ffmpeg is installed and ready to use.
import os
import subprocess

import config as cfg


### POST-PROCESSING ###
def stack_eyes(left_fp, right_fp, out_fp):
	"""
	Stack two eyes horizontally.
	Returns True on success, and None otherwise.
	To use this function, put the following into post_process(n):
	
		if n % 2 == 1:
			postprocessing.stack_eyes(
				OUTPUT + PARTS[n - 1][0] + '.mp4',
				OUTPUT + PARTS[n][0] + '.mp4',
				(FINAL_OUTPUT + PARTS[n][0] + '.mp4').replace('R_', 'ALL_')
			)
	
	Note that the above example assumes that the parts in PARTS are arranged
	so that every left-eye part is immediately followed by its right-eye part, e.g.:
		
		PARTS = [
			('L_TOP', -1, -90, 0, -90, 0),
			('R_TOP', 1, -90, 0, -90, 0),
			...
		]
	
	This is the case with the example config.
	"""
	print('Running ffmpeg to stitch eyes together...')
	p = subprocess.run([
		'ffmpeg', '-i', left_fp, '-i', right_fp, '-filter_complex', 'hstack',
		'-vcodec', 'libx264', out_fp
	])
	if p.returncode == 0:
		print('Done, removing the LEFT and RIGHT files')
		os.remove(left_fp)
		os.remove(right_fp)
		return True


def combine_five_parts(front_fp, top_fp, bottom_fp, left_fp, right_fp, output_fp, audio_fp=None):
	"""
	Combine the five angles of a VR180 video into one.
	This function relies on the presence of the ``masks`` directory containing .png files
	in the same directory as this file (which is the case if you've cloned this repo from GitHub).
	"""
	ffmpeg_args = [
		'ffmpeg',
		# Input videos
		'-i', front_fp, '-i', top_fp, '-i', bottom_fp, '-i', left_fp, '-i', right_fp,
		# Start of filtergraph
		'-filter_complex',
		# Extract the alpha channel from mask inputs
		'movie=masks/vr180mask_front.png[FrontMaskIn];'
		'[FrontMaskIn][0]scale2ref[FrontMaskScaled][Front];'
		'[FrontMaskScaled]format=pix_fmts=yuva444p,alphaextract[FrontMask];'
		
		'movie=masks/vr180mask_t_small.png[TopMaskIn];'
		'[TopMaskIn][1]scale2ref[TopMaskScaled][Top];'
		'[TopMaskScaled]format=pix_fmts=yuva444p,alphaextract[TopMask];'
		
		'movie=masks/vr180mask_b_small.png[BottomMaskIn];'
		'[BottomMaskIn][2]scale2ref[BottomMaskScaled][Bottom]'
		';[BottomMaskScaled]format=pix_fmts=yuva444p,alphaextract[BottomMask];'
		
		'movie=masks/vr180mask_left.png[LeftMaskIn];'
		'[LeftMaskIn][3]scale2ref[LeftMaskScaled][Left];'
		'[LeftMaskScaled]format=pix_fmts=yuva444p,alphaextract[LeftMask];'
		# Merge gray masks with input videos
		'[Front][FrontMask]alphamerge[FrontOut];'
		'[Top][TopMask]alphamerge[TopOut];'
		'[Bottom][BottomMask]alphamerge[BottomOut];'
		'[Left][LeftMask]alphamerge[LeftOut];'
		## Overlay all 5 parts in order
		'[4][LeftOut]overlay=shortest=1[RL];'
		'[RL][BottomOut]overlay=shortest=1[RLB];'
		'[RLB][TopOut]overlay=shortest=1[RLBT];'
		'[RLBT][FrontOut]overlay=shortest=1[out]',
		# Output parameters
		'-map', '[out]:v',
		output_fp
	]
	if audio_fp:
		ffmpeg_args.insert(-3, '-i')
		ffmpeg_args.insert(-3, audio_fp)
		ffmpeg_args.insert(-3, '-map')
		ffmpeg_args.insert(-3, '5:a')
	p = subprocess.run(ffmpeg_args)


### SPLIT MANAGEMENT ###
# To use the following two functions, make sure that the following:
#
# split_files = []
#
# (without the # sign) exists somewhere in config.py and outside of a function.
# In the example config, it's right above "def after_split(fp)".

def convert_split(in_fp, out_fp=None):
	"""
	Convert a single split from .avi to .mp4.
	Returns True on success, and None otherwise.
	To use this function, put the following into after_split(fp):
	
		postprocessing.convert_split(fp)
	
	"""
	print('Running ffmpeg to convert AVI to MP4...')
	out_fp = out_fp or in_fp.replace('.avi', '.mp4')
	p = subprocess.run([
			'ffmpeg', '-i', in_fp, '-vcodec', 'libx264', out_fp
		])
	if p.returncode == 0:
		print('Done, removing the AVI file')
		os.remove(in_fp)
		cfg.split_files.append(out_fp)
		return True


def concat_splits(out_fp):
	"""
	Concatenate splits with identical codecs.
	Returns True on success, and None otherwise.
	To use this function, put the following into merge_splits(n):
	
		postprocessing.concat_splits(OUTPUT + PARTS[n][0] + '.mp4')
	
	Alternatively, if you want to also do post-processing
	(such as stacking the eyes), put the following instead:
	
		if postprocessing.concat_splits(OUTPUT + PARTS[n][0] + '.mp4'):
			post_process(n)
	
	"""
	print('Running ffmpeg to merge splits...')
	with open(f'/tmp/PyAutoMMDVRRender', 'w+') as f:
		for fp in cfg.split_files:
			f.write(f'file \'{fp}\'\n')
	p = subprocess.run([
		'ffmpeg', '-f', 'concat', '-safe', '0', '-i', '/tmp/PyAutoMMDVRRender', '-c', 'copy',
		out_fp
	])
	if p.returncode == 0:
		print('Done, removing the original split files')
		for fp in cfg.split_files:
			os.remove(fp)
		cfg.split_files.clear()
		return True
