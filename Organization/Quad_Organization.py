Rmport numpy as np
from .Organization import Organization

class Quad_Organization(Organization):

    def vote_once(self, work_id):
        quad_token_const = self.configs[quad_token_const]
        for member in self.members:
            vote = member.decide(self.works[work_id])
            self.reduce_member_token(quad_token_const * vote * vote)
            work.votes.append(vote)
        work.voted = True
        if sum(work.votes) > 0:
            work.ans = True
        else:
            work.ans = False
        self.update_token(work_id)
        self.del_work(work_id)
