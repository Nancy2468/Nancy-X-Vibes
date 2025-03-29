from datetime import datetime, timedelta
import threading
import time

class QueueManager:
    def __init__(self):
        self.queues = {}
        self.current_songs = {}
        self.current_positions = {}
        self.last_activity = {}
        self.auto_stop_thread = threading.Thread(target=self._check_inactivity, daemon=True)
        self.auto_stop_thread.start()

    def add_to_queue(self, group_id, song):
        if len(self.queues.get(group_id, [])) < 10:
            self.queues.setdefault(group_id, []).append(song)
            self._send_emoji_and_sticker(group_id)
        else:
            # Notify user that the queue is full
            pass

    def play_next(self, group_id):
        if self.queues.get(group_id):
            self.current_songs[group_id] = self.queues[group_id].pop(0)
            self.current_positions[group_id] = 0  # Reset position for new song
            # Code to play self.current_songs[group_id] from the beginning
        else:
            # Prompt last requester to add more songs
            pass

    def _send_emoji_and_sticker(self, group_id):
        # Code to send emoji and sticker
        pass

    def change_song_position(self, group_id, old_index, new_index):
        if 0 <= old_index < len(self.queues.get(group_id, [])) and 0 <= new_index < len(self.queues.get(group_id, [])):
            song = self.queues[group_id].pop(old_index)
            self.queues[group_id].insert(new_index, song)

    def remove_from_queue(self, group_id, index):
        if 0 <= index < len(self.queues.get(group_id, [])):
            self.queues[group_id].pop(index)

    def play(self, group_id):
        pass  # Code to play the current song

    def pause(self, group_id):
        pass  # Code to pause the current song

    def resume(self, group_id):
        pass  # Code to resume the paused song

    def stop(self, group_id):
        self.current_songs[group_id] = None
        self.current_positions[group_id] = 0

    def seek(self, group_id, seconds):
        self.current_positions[group_id] = seconds
        pass  # Code to seek to a specific time in the current song

    def set_volume(self, group_id, volume):
        pass  # Code to set the volume of the current song

    def _check_inactivity(self):
        while True:
            for group_id in list(self.last_activity.keys()):
                if datetime.utcnow() - self.last_activity[group_id] > timedelta(minutes=6):
                    self.stop(group_id)
                    # Notify group that songs have been stopped due to inactivity
                    self.last_activity[group_id] = datetime.utcnow()  # Reset the activity timer
            time.sleep(60)

    def update_activity(self, group_id):
        self.last_activity[group_id] = datetime.utcnow()

    def resume_or_restart(self, group_id, choice):
        if choice == 'resume' and self.current_songs.get(group_id):
            self.seek(group_id, self.current_positions[group_id])
            self.play(group_id)
        elif choice == 'restart':
            self.play_next(group_id)
