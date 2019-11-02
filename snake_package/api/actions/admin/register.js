/**
 * Created by isaac on 2/21/16.
 */
import mongoose from 'mongoose';
import jwt from 'jsonwebtoken';
import config from '../../config';
const Admin = mongoose.model('Admin');

export default function register(req) {

  return new Promise((resolve, reject) => {

    const { name, password } = req.body;
    if (name && password) {

      Admin.findOne({ name }, (err, doc) => {
        if (doc) {
          reject({
            msg: '此昵称已经被占用了!'
          });
        } else {
          const user = new Admin({ name });
          user.password = user.generateHash(password);

          user.save(err => {
            if (err) reject({ msg: '用户注册失败!', err });

            user.password = null;

            const _user = {
              _id: user._id,
              password: user.password,
              name: user.name,
              groups: user.groups,
              friends: user.friends,
              role: user.role,
              create_time: user.create_time
            };
            // req.session.user = user;
            const token = jwt.sign(
                _user,
                config.tokenSecret,
                { expiresIn: config.tokenMaxAge }
            );
            resolve({ user, token });
          });
        }
      });
    } else {
      reject({ msg: '缺少用户名或密码!' });
    }
  });
}