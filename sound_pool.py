import sound, sound_positioning, random
class sound_pool_item:

    def __init__(self, filename, id, listener_x, listener_y, listener_z, listener_angle, minx, maxx, miny, maxy, minz, maxz, dimension, looping, persistent, pan_step, volume_step, behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, autoplay):
        self.handle = sound.sound()
        self.filename = filename
        self.id = id
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz
        self.dimension = dimension
        self.looping = looping
        self.persistent = persistent
        self.pan_step = pan_step
        self.volume_step = volume_step
        self.behind_pitch_decrease = behind_pitch_decrease
        self.start_pan = start_pan
        self.start_pitch = start_pitch
        self.start_volume = start_volume
        self.paused = False
        try: self.handle.load(filename)
        except:
            self.handle=-1
            return
        self.handle.pitch = start_pitch
        self.update(listener_x, listener_y, listener_z, listener_angle)
        if autoplay:
            if looping:
                self.handle.play_looped()
            else:
                self.handle.play()

    def update_sound(self, dimension, minx, maxx, miny, maxy, minz, maxz):
        self.dimension = dimension
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxy
        self.minz = minz
        self.maxz = maxz

    def update_start_values(self, start_pan, start_volume, start_pitch):
        self.start_pan = start_pan
        self.start_volume = start_volume
        self.start_pitch = start_pitch

    def pause(self):
        if not self.handle.is_playing:
            return False
        else:
            self.paused = True
            self.handle.pause()
            return True

    def resume(self):
        if not self.paused:
            return False
        else:
            self.paused = False
            if self.looping:
                self.handle.play_looped()
            else:
                self.play()
            return True

    def is_playing(self):
        return self.handle.is_playing

    def update(self, listener_x, listener_y, listener_z, listener_angle):
        source_x = 0
        source_y = 0
        source_z = 0
        if listener_x > self.maxx:
            source_x = self.maxx
        else:
            if listener_x < self.minx:
                source_x = self.minx
            else:
                source_x = listener_x
        if listener_y > self.maxy:
            source_y = self.maxy
        else:
            if listener_y < self.miny:
                source_y = self.miny
            else:
                source_y = listener_y
        if listener_z > self.maxz:
            source_z = self.maxz
        else:
            if listener_z < self.minz:
                source_z = self.minz
            else:
                source_z = listener_z
        if self.dimension == 1:
            sound_positioning.position_sound_custom_1d(self.handle, listener_x, source_x, self.pan_step, self.volume_step, self.start_pan, self.start_volume)
        else:
            if self.dimension == 2:
                sound_positioning.position_sound_custom_2d(self.handle, listener_x, listener_y, source_x, source_y, listener_angle, self.pan_step, self.volume_step, self.behind_pitch_decrease, self.start_pan, self.start_volume, self.start_pitch)
            else:
                if self.dimension == 3:
                    sound_positioning.position_sound_custom_3d(self.handle, listener_x, listener_y, listener_z, source_x, source_y, source_z, listener_angle, self.pan_step, self.volume_step, self.behind_pitch_decrease, self.start_pan, self.start_volume, self.start_pitch)
                else:
                    if self.dimension == 0:
                        self.handle.pan = self.start_pan
                        self.handle.volume = self.start_volume
                        self.handle.pitch = self.start_pitch

    def destroy(self):
        self.handle.close()


class sound_pool:

    def __init__(self):
        self.items = []
        self.pan_step = 20
        self.volume_step = 2
        self.behind_pitch_decrease = -5
        self.is_cleaning = False
        self.packname=""
    def play_stationary(self, filename, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_stationary_extended(self, filename, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_1d(self, filename, listener_x, sound_x, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, 0, 0, 0, sound_x, sound_x, 0, 0, 0, 0, 1, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_1d_extended(self, filename, listener_x, sound_x, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, 0, 0, 0, sound_x, sound_x, 0, 0, 0, 0, 1, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_1d(self, filename, listener_x, sound_minx, sound_maxx, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, 0, 0, 0, sound_minxx, sound_maxx, 0, 0, 0, 0, 1, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_1d_extended(self, filename, listener_x, sound_minx, sound_maxx, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, 0, 0, 0, sound_minx, sound_maxx, 0, 0, 0, 0, 1, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_2d(self, filename, listener_x, listener_y, listener_angle, sound_x, sound_y, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, 0, listener_angle, sound_x, sound_x, sound_y, sound_y, 0, 0, 2, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_2d_extended(self, filename, listener_x, listener_y, listener_angle, sound_x, sound_y, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, 0, listener_angle, sound_x, sound_x, sound_y, sound_y, 0, 0, 2, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_2d(self, filename, listener_x, listener_y, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, 0, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, 0, 0, 2, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_2d_extended(self, filename, listener_x, listener_y, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, 0, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, 0, 0, 2, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_3d(self, filename, listener_x, listener_y, listener_z, listener_angle, sound_x, sound_y, sound_z, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, listener_z, listener_angle, sound_x, sound_x, sound_y, sound_y, sound_z, sound_z, 3, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_3d_extended(self, filename, listener_x, listener_y, listener_z, listener_angle, sound_x, sound_y, sound_z, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, listener_z, listener_angle, sound_x, sound_x, sound_y, sound_y, sound_z, sound_z, 3, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_3d(self, filename, listener_x, listener_y, listener_z, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz, looping, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, listener_z, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz, 3, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, 0, 0, 0, 100, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def play_src_3d_extended(self, filename, listener_x, listener_y, listener_z, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz, looping, start_offset, start_pan, start_volume, start_pitch, persistent=False):
        s = sound_pool_item(self.packname+filename, self.get_id(), listener_x, listener_y, listener_z, listener_angle, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz, 3, looping, persistent, self.pan_step, self.volume_step, self.behind_pitch_decrease, start_offset, start_pan, start_volume, start_pitch, True)
        if s.handle!=-1: self.items.append(s)
        self.clean()
        return s.id

    def destroy_all(self):
        for i in self.items:
            i.destroy()

        self.items = []

    def get_item(self, id):
        for i in self.items:
            if id == i.id:
                return i

        return 0

    def destroy(self, id):
        i = self.get_item(id)
        if i == 0:
            return False
        i.destroy()
        self.items.remove(i)

    def update_sound_start_values(self, id, start_pan, start_volume, start_pitch):
        i = self.get_item(id)
        if i == 0:
            return False
        i.update_start_values(start_pan, start_volume, start_pitch)

    def update_sound_1d(self, id, sound_x):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(1, sound_x, sound_x, 0, 0, 0, 0)

    def update_sound_src_1d(self, id, sound_minx, sound_maxx):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(1, sound_minx, sound_maxx, 0, 0, 0, 0)

    def update_sound_2d(self, id, sound_x, sound_y):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(2, sound_x, sound_x, sound_y, sound_y, 0, 0)

    def update_sound_src_2d(self, id, sound_minx, sound_maxx, sound_miny, sound_maxy):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(2, sound_minx, sound_maxx, sound_miny, sound_maxy, 0, 0)

    def update_sound_3d(self, id, sound_x, sound_y, sound_z):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(3, sound_x, sound_x, sound_y, sound_y, sound_z, sound_z)

    def update_sound_src_3d(self, id, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz):
        i = self.get_item(id)
        if i == 0:
            return
        i.update_sound(3, sound_minx, sound_maxx, sound_miny, sound_maxy, sound_minz, sound_maxz)

    def pause_sound(self, id):
        i = self.get_item(id)
        if i == 0:
            return False
        else:
            return i.pause()

    def resume_sound(self, id):
        i = self.get_item(id)
        if i == 0:
            return False
        else:
            return i.resume()

    def update_listener_1d(self, x):
        for i in self.items:
            i.update(x, 0, 0, 0.0)

        self.clean()

    def update_listener_2d(self, x, y, angle=0.0):
        for i in self.items:
            i.update(x, y, 0, angle)

        self.clean()

    def update_listener_3d(self, x, y, z, angle=0.0):
        for i in self.items:
            i.update(x, y, z, angle)

        self.clean()

    def clean(self):
        if self.is_cleaning:
            return
        self.is_cleaning = True
        marked_items = []
        for i in self.items:
            if not i.looping:
                if i.persistent:
                    pass
                else:
                    if not i.is_playing():
                        if not i.paused:
                            marked_items.append(i)

        for i in marked_items:
            i.destroy()
            self.items.remove(i)

        self.is_cleaning = False

    def get_id(self):
        id = random.randint(100000000, 999999999)
        tries = 0
        while self.get_item(id) != 0:
            if tries < 500:
                id = random.randint(100000000, 999999999)
                tries += 1

        if tries >= 500:
            return -1
        else:
            return id
    def set_pack_name(self,name):
        self.packname=name

p=sound_pool()
p.set_pack_name("sounds/")