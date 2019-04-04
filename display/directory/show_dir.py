# -*- coding:utf-8 -*-
import os, json
import time
import datetime


def TimeStampToTime(timestamp):
  timestamp += 8*3600
  timeStruct = time.localtime(timestamp)
  return time.strftime('%Y-%m-%d %H:%M:%S',timeStruct)


def get_FileSize(filePath):
  fsize = os.path.getsize(filePath)
  fsize = fsize/float(1024)
  if fsize < 1024:
    return str(round(fsize)) + 'K'
  else:
    return str(round(fsize/float(1024), 1)) + 'M'


def get_FileModifyTime(filePath):
  filePath.encode("utf8")
  mtime = os.stat(filePath)
  return TimeStampToTime(mtime.st_mtime)


def get_dirname(dirname):
  date = dirname.split('_')[-1]
  return date[:-2] + '/' + date[-2:]


def list_dir(path, res):
  for i in os.listdir(path):
    temp_dir = os.path.join(path, i)
    if '/.' in temp_dir:
      continue
    if os.path.isdir(temp_dir):
      temp = {"dirname": temp_dir.split('/')[-1], "dirname_s": get_dirname(temp_dir.split('/')[-1]), 'child_dirs': [], 'files': []}
      res['child_dirs'].append(list_dir(temp_dir, temp))
    else:
      mtime = get_FileModifyTime(temp_dir)
      size = get_FileSize(temp_dir)
      if 'pdf' in path:
        date_list = str(i.split(' ')[-1]).split('.')[0].split('-')
        res['files'].append({'filename': i, 'filename_s': date_list[0] + '/' + date_list[1] + '/' + date_list[2], 'ctime': mtime, 'size': size})
      elif 'Monthly_Reports' in path:
        date = str(i.split('-')[-2])
        type = str(i.split('-')[-1]).split('.')[0]
        res['files'].append({'filename': i, 'filename_s': date[:-2] + '/' + date[-2:] + '-' + type, 'ctime': mtime, 'size': size})
      else:
        res['files'].append(i)
  return res


def get_origin_dirs(dirname):
  res = {'dirname': dirname, 'child_dirs': [], 'files': []}
  return list_dir('../daily_report/' + dirname + '/', res)


if __name__ == '__main__':
    print(json.dumps(get_origin_dirs('pdf')))
